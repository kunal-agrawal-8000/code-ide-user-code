"""
Twitter Clone Backend - Main Application
A simple Twitter clone with basic functionality for posting tweets,
following users, and viewing timelines.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for demo purposes
users = {}
tweets = []
followers = {}

class TwitterClone:
    """Main Twitter clone class with core functionality."""
    
    def __init__(self):
        self.users = {}
        self.tweets = []
        self.followers = {}
    
    def create_user(self, username, email, profile_data):
        """Create a new user profile."""
        if username in self.users:
            return {"error": "User already exists"}
        
        self.users[username] = {
            "username": username,
            "email": email,
            "profile": profile_data,
            "created_at": datetime.now().isoformat(),
            "tweet_count": 0,
            "follower_count": 0,
            "following_count": 0
        }
        return {"success": "User created successfully"}
    
    def post_tweet(self, username, content, hashtags=None):
        """Post a new tweet."""
        if username not in self.users:
            return {"error": "User not found"}
        
        tweet = {
            "id": len(self.tweets) + 1,
            "username": username,
            "content": content,
            "hashtags": hashtags or [],
            "timestamp": datetime.now().isoformat(),
            "likes": 0,
            "retweets": 0,
            "replies": []
        }
        
        self.tweets.append(tweet)
        self.users[username]["tweet_count"] += 1
        return {"success": "Tweet posted successfully", "tweet_id": tweet["id"]}
    
    def follow_user(self, follower, following):
        """Follow another user."""
        if follower not in self.users or following not in self.users:
            return {"error": "User not found"}
        
        if follower not in self.followers:
            self.followers[follower] = []
        
        if following not in self.followers[follower]:
            self.followers[follower].append(following)
            self.users[follower]["following_count"] += 1
            self.users[following]["follower_count"] += 1
            return {"success": "User followed successfully"}
        
        return {"error": "Already following this user"}
    
    def get_timeline(self, username, limit=10):
        """Get user's timeline with tweets from followed users."""
        if username not in self.users:
            return {"error": "User not found"}
        
        following = self.followers.get(username, [])
        following.append(username)  # Include own tweets
        
        timeline = [
            tweet for tweet in self.tweets 
            if tweet["username"] in following
        ]
        
        # Sort by timestamp (most recent first)
        timeline.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {"timeline": timeline[:limit]}

# API Routes
@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user account."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    profile = data.get('profile', {})
    
    twitter_clone = TwitterClone()
    result = twitter_clone.create_user(username, email, profile)
    return jsonify(result)

@app.route('/api/tweets', methods=['POST'])
def post_tweet():
    """Post a new tweet."""
    data = request.get_json()
    username = data.get('username')
    content = data.get('content')
    hashtags = data.get('hashtags', [])
    
    twitter_clone = TwitterClone()
    result = twitter_clone.post_tweet(username, content, hashtags)
    return jsonify(result)

@app.route('/api/follow', methods=['POST'])
def follow_user():
    """Follow another user."""
    data = request.get_json()
    follower = data.get('follower')
    following = data.get('following')
    
    twitter_clone = TwitterClone()
    result = twitter_clone.follow_user(follower, following)
    return jsonify(result)

@app.route('/api/timeline/<username>')
def get_timeline(username):
    """Get user's timeline."""
    limit = request.args.get('limit', 10, type=int)
    
    twitter_clone = TwitterClone()
    result = twitter_clone.get_timeline(username, limit)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)