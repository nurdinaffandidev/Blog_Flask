import pytest
from flask_blog import create_app, db
from flask_blog.models import User
from flask_bcrypt import Bcrypt
from flask_blog.config import TestingConfig

"""
Test Configuration Module for Flask Blog Application
=====================================================

This module contains reusable pytest fixtures to facilitate testing
of the Flask Blog application. It includes setup for a testing
application instance, a test client for simulating requests, and
a sample user for authentication-related tests.

Fixtures:
---------

1. app:
    - Purpose: Creates and configures a Flask application instance
      with testing settings.
    - Features:
        - Enables testing mode.
        - Uses in-memory SQLite database for speed and isolation.
        - Disables CSRF protection for easier form testing.
    - Behavior:
        - Sets up the database before tests.
        - Tears down and cleans up the database after tests.

2. client:
    - Purpose: Provides a Flask test client for simulating HTTP
      requests to routes.
    - Dependency: Requires the `app` fixture.

3. test_user:
    - Purpose: Inserts a sample user into the database for testing
      login, authentication, and user-based logic.
    - Behavior:
        - Hashes a password using Flask-Bcrypt.
        - Adds and commits a User model instance to the database.
    - Returns:
        - A `User` instance with preconfigured credentials:
          Username: `testuser`, Email: `test@example.com`,
          Password: `'password'` (hashed).
"""

# Fixture to set up Flask app in testing mode
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestingConfig)  # Use your custom testing config
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory DB for fast, isolated tests
        'WTF_CSRF_ENABLED': False  # Disable CSRF for form tests
    })

    with app.app_context():
        db.create_all()          # Create all tables
        yield app                # Provide app to tests
        db.session.remove()     # Cleanup DB session
        db.drop_all()           # Drop all tables after tests


# Fixture to provide a test client for simulating HTTP requests
@pytest.fixture
def client(app):
    """Flask test client for simulating HTTP requests."""
    return app.test_client()


# Fixture to create a sample test user in the database
@pytest.fixture
def test_user(app):
    """Create a test user and add to the test database."""
    bcrypt = Bcrypt(app)
    user = User(username='testuser', email='test@example.com')
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user.password = hashed_password
    db.session.add(user)
    db.session.commit()
    return user
