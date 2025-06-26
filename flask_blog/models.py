from datetime import datetime, timezone
from flask_blog import db, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app

'''
Login Manager extension will expect User model to have certain attributes and methods
4 attributes:
    1. is_authenticated
    2. is_active
    3. is_anonymous
    4. get_id
Use inherited class UserMixin for ease of implementation
'''
# decorator function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # creating one-to-many relationship to Post
    # backref: similar to adding another column to Post model, using 'author' attribute get User that created Post
    # lazy: defines when SQLAlchemy loads data from db. True: loads data as necessary in one go
    # 'Post' uppercased as referencing to Post class
    post = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        """
        Generates a time-sensitive token for password reset or email confirmation.

        This token is typically sent to the user's email and can be used to securely
        verify their identity when resetting a password or activating an account.

        Returns:
            str: A URL-safe, signed token containing the user's ID.
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps({'user_id': self.id})
        return token

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """
        Validates a password reset token and returns the corresponding user.

        The method attempts to deserialize the token using the application's
        secret key and checks if the token has expired. It handles common
        exceptions such as expired or tampered tokens.

        Args:
            token (str): The token to validate.
            expires_sec (int, optional): The token's maximum age in seconds.
                                         Defaults to 1800 (30 minutes).

        Returns:
            User | None: The user associated with the token if valid,
            or None if the token is expired, invalid, or an error occurs.
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token, max_age=expires_sec)['user_id']
        except SignatureExpired:
            print("✅ Token expired.")
            return None
        except BadSignature:
            print("❌ Token is invalid.")
            return None
        except Exception:
            print("⚠️ Unknown error.")
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User(username: '{self.username}',email: '{self.email}',image_file: '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    # linking many-to-one relationship to User
    # 'user-id' lowercased as referencing table name and column name which are automatically set to lowercased
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post(title: '{self.title}',date_posted: '{self.date_posted}')"
