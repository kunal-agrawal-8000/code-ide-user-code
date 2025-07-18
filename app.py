#!/usr/bin/env python3
"""
Twitter Clone Application
A simple Twitter-like social media application built with Flask
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_clone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    space_uuid = db.Column(db.String(36))
    
    # Relationships
    tweets = db.relationship('Tweet', backref='author', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'author': self.author.username,
            'author_id': self.user_id
        }

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    """Home page showing timeline"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Get tweets from followed users and own tweets
    following_ids = [f.followed_id for f in user.following]
    following_ids.append(user.id)  # Include own tweets
    
    tweets = Tweet.query.filter(Tweet.user_id.in_(following_ids)).order_by(Tweet.timestamp.desc()).limit(50).all()
    
    return render_template('timeline.html', user=user, tweets=tweets, current_user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/tweet', methods=['POST'])
def post_tweet():
    """Post a new tweet"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    content = request.form['content']
    if content.strip():
        tweet = Tweet(content=content, user_id=session['user_id'])
        db.session.add(tweet)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/profile/<username>')
def profile(username):
    """User profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=username).first_or_404()
    current_user = User.query.get(session['user_id'])
    
    tweets = Tweet.query.filter_by(user_id=user.id).order_by(Tweet.timestamp.desc()).limit(20).all()
    
    is_following = Follow.query.filter_by(follower_id=current_user.id, followed_id=user.id).first() is not None
    
    follower_count = Follow.query.filter_by(followed_id=user.id).count()
    following_count = Follow.query.filter_by(follower_id=user.id).count()
    
    return render_template('profile.html', 
                         user=user, 
                         current_user=current_user, 
                         tweets=tweets,
                         is_following=is_following,
                         follower_count=follower_count,
                         following_count=following_count)

@app.route('/follow/<username>')
def follow_user(username):
    """Follow a user"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_to_follow = User.query.filter_by(username=username).first_or_404()
    current_user = User.query.get(session['user_id'])
    
    if user_to_follow.id == current_user.id:
        flash("You can't follow yourself!")
        return redirect(url_for('profile', username=username))
    
    existing_follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_to_follow.id).first()
    
    if not existing_follow:
        follow = Follow(follower_id=current_user.id, followed_id=user_to_follow.id)
        db.session.add(follow)
        db.session.commit()
        flash(f'You are now following {username}!')
    
    return redirect(url_for('profile', username=username))

@app.route('/unfollow/<username>')
def unfollow_user(username):
    """Unfollow a user"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_to_unfollow = User.query.filter_by(username=username).first_or_404()
    current_user = User.query.get(session['user_id'])
    
    follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_to_unfollow.id).first()
    
    if follow:
        db.session.delete(follow)
        db.session.commit()
        flash(f'You are no longer following {username}!')
    
    return redirect(url_for('profile', username=username))

@app.route('/api/tweets')
def api_tweets():
    """API endpoint for tweets"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    following_ids = [f.followed_id for f in user.following]
    following_ids.append(user.id)
    
    tweets = Tweet.query.filter(Tweet.user_id.in_(following_ids)).order_by(Tweet.timestamp.desc()).limit(50).all()
    
    return jsonify([tweet.to_dict() for tweet in tweets])

def load_existing_users():
    """Load existing users from UserDetails.json files"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Look for existing user directories
    for item in os.listdir(base_path):
        if item.startswith('@'):
            user_dir = os.path.join(base_path, item)
            if os.path.isdir(user_dir):
                json_path = os.path.join(user_dir, 'undefined', 'UserDetails.json')
                if os.path.exists(json_path):
                    try:
                        with open(json_path, 'r') as f:
                            user_data = json.load(f)
                            username = user_data.get('username', '').replace('@', '')
                            space_uuid = user_data.get('space_uuid', '')
                            
                            # Check if user already exists
                            if not User.query.filter_by(username=username).first():
                                user = User(
                                    username=username,
                                    email=f"{username}@example.com",
                                    password_hash=generate_password_hash("password123"),
                                    space_uuid=space_uuid
                                )
                                db.session.add(user)
                                print(f"Added user: {username}")
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error loading user data from {json_path}: {e}")
    
    db.session.commit()

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        load_existing_users()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)