from flask_blog.users.forms import RegistrationForm
from flask_blog.models import User
from flask_blog import db
from flask_bcrypt import Bcrypt


"""
Unit tests for RegistrationForm in flask_blog.users.forms.

These tests focus on custom validation logic, particularly:
    - Ensuring the username is unique during registration.
    - Ensuring valid input data passes validation.

Tests:
    - test_registration_form_validates_unique_user:
        Adds a user to the test database and verifies that the form correctly
        rejects a new registration with the same username.

    - test_registration_form_accepts_valid_data:
        Ensures that the form validates successfully when provided with valid
        and unique user data.
"""

def test_registration_form_validates_unique_user(app):
    """
        Test that RegistrationForm fails validation when the username is already taken.

        Steps:
           1. Create and commit a user to simulate an existing account.
           2. Submit the registration form with the same username but a new email.
           3. Assert that form validation fails and a proper error message appears.

        Args:
            app: Flask application fixture.
   """
    with app.app_context():
        # Add a user to simulate a taken username
        user = User(username="existinguser", email="existing@example.com")
        bcrypt = Bcrypt(app)
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()

        form = RegistrationForm(
            username="existinguser",
            email="new@example.com",
            password="password",
            confirm_password="password"
        )
        assert not form.validate()
        assert 'This username is taken' in str(form.username.errors)


def test_registration_form_accepts_valid_data(app):
    """
        Test that RegistrationForm validates successfully with new, valid user data.

        Args:
            app: Flask application fixture.
    """
    with app.app_context():
        form = RegistrationForm(
            username="newuser",
            email="new@example.com",
            password="password",
            confirm_password="password"
        )
        assert form.validate() is True