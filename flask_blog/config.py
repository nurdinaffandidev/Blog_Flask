import os


class Config:
    """
       Base configuration class for the Flask application.

       This class holds default configuration settings such as:
       - Secret key for session and CSRF protection
       - Database connection URI
       - Email server settings for sending emails

       Environment Variables:
           FLASK_SECRET_KEY (str): Secret key for securing sessions and forms.
           FLASK_SQLALCHEMY_DATABASE_URI (str): Database URI (e.g., sqlite:///site.db).
           EMAIL_USER (str): Email address used to send emails (e.g., noreply@demo.com).
           EMAIL_PASS (str): Password or app-specific password for the email account.
    """
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


class TestingConfig:
    """
        Configuration settings for running tests with the Flask application.

        Attributes:
            TESTING (bool): Enables testing mode for Flask, which provides better error reporting.
            SQLALCHEMY_DATABASE_URI (str): Uses an in-memory SQLite database to ensure isolated, fast test runs.
            SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables modification tracking to save resources during tests.
            WTF_CSRF_ENABLED (bool): Disables CSRF protection in WTForms to simplify form testing.
            SECRET_KEY (str): Secret key used by Flask for session management during testing.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testing-secret'