import os


class Config:
    # Configure secret key:
    # Secret key will protect against modifying cookies and cross-site request forgery (csrf) attacks
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    # Configure database:
    # Using SQLite as easiest to set up and will simply be a file on our file system
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_SQLALCHEMY_DATABASE_URI')
    # configure email server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')