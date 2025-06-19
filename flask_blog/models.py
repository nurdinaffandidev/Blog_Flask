from datetime import datetime, timezone
from flask_blog import db

class User(db.Model):
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
