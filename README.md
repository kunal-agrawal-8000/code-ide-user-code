# Twitter Clone 🐦

A simple Twitter-like social media application built with Flask, featuring user authentication, tweet posting, following/followers, and a responsive web interface.

## Features ✨

- **User Authentication**: Registration and login system with password hashing
- **Tweet Posting**: Create and share tweets with a 280-character limit
- **Timeline**: View tweets from followed users in chronological order
- **User Profiles**: View user profiles with tweet history and stats
- **Follow System**: Follow and unfollow other users
- **Responsive Design**: Clean, modern UI with Bootstrap styling
- **Real-time Updates**: Character counter and live timeline updates

## Screenshots 📸

### Login Page
![Login Page](https://github.com/user-attachments/assets/068edf45-0704-4829-86c4-5c1c95f5ee3d)

### Main Timeline
![Timeline](https://github.com/user-attachments/assets/6d60631e-57db-4cce-8dcc-998b306158f4)

## Installation & Setup 🚀

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd code-ide-user-code
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 app.py
   ```

4. **Open in browser**:
   Navigate to `http://127.0.0.1:5000`

## Usage 📝

### Getting Started
1. **Register**: Create a new account or use existing users (kunal_me, kunal1122 with password: password123)
2. **Login**: Access your account with username and password
3. **Post Tweet**: Share your thoughts with the "What's happening?" composer
4. **Follow Users**: Visit user profiles and follow them to see their tweets
5. **Timeline**: View tweets from people you follow on your home timeline

### Default Users
The application loads existing users from the UserDetails.json files:
- `kunal_me` (password: password123)
- `kunal1122` (password: password123)

## Technical Details 🔧

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Werkzeug password hashing
- **Icons**: Font Awesome

### Database Schema
- **Users**: id, username, email, password_hash, bio, joined_date, space_uuid
- **Tweets**: id, content, timestamp, user_id
- **Follows**: id, follower_id, followed_id, timestamp

### API Endpoints
- `GET /` - Home timeline (authenticated)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration
- `GET /logout` - Logout user
- `POST /tweet` - Post new tweet
- `GET /profile/<username>` - User profile
- `GET /follow/<username>` - Follow user
- `GET /unfollow/<username>` - Unfollow user
- `GET /api/tweets` - JSON API for tweets

## File Structure 📁

```
code-ide-user-code/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_app.py           # Basic functionality tests
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── timeline.html
│   └── profile.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── @kunal_me/           # User directories (existing)
    └── undefined/
        └── UserDetails.json
```

## Testing 🧪

Run the test suite:
```bash
python3 test_app.py
```

## Features in Action 🎬

1. **Registration & Login**: Secure user authentication with password hashing
2. **Tweet Composer**: Real-time character counting with 280-character limit
3. **Timeline**: Displays tweets from followed users in chronological order
4. **User Profiles**: Shows user info, tweet count, follower/following stats
5. **Follow System**: Follow/unfollow functionality with real-time updates
6. **Responsive Design**: Works on desktop and mobile devices

## Security Features 🔒

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection through Flask's built-in security
- SQL injection prevention with SQLAlchemy ORM
- XSS protection through template escaping

## Future Enhancements 🔮

- Like/retweet functionality
- Image uploads
- Direct messaging
- Search functionality
- User mentions and hashtags
- Email notifications
- Profile editing
- Tweet deletion

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source and available under the MIT License.