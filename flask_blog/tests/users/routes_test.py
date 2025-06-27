from unittest.mock import patch

import pytest
from flask import url_for

# -------------------
# Register Route Test
# -------------------
def test_register_get(client):
    """
        Tests GET request for registration page.
        Confirms the route loads and contains "Register" in HTML.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
    """
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_post(client):
    """
        Simulates form submission to register a new user.
        follow_redirects=True follows the redirect to the login page.
        Confirms a flash message appears.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
    """
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'Account created for Newuser' in response.data

# ---------------
# Login Test
# ---------------
def test_login_valid_user(client, test_user):
    """
        Logs in the predefined test_user with correct password.
        Expects a success flash message.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
            test_user: pytest fixture that provides a simulated user for testing your Flask app.
    """
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert b'Logged in for account test@example.com' in response.data


def test_login_invalid_user(client):
    """
        Attempts login with invalid credentials.
        Expects an error flash message.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
    """
    response = client.post('/login', data={
        'email': 'wrong@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Invalid login credentials' in response.data

# -------------------
# Logout Test
# -------------------
def test_logout(client, test_user):
    """
        Logs in the user, then logs out.
        Verifies the response content after logout (e.g., that the home page is shown).

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
            test_user: pytest fixture that provides a simulated user for testing your Flask app.
    """
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    response = client.get('/logout', follow_redirects=True)
    assert b'Home' in response.data  # Assuming main.index renders 'Home' text

# -------------------
# Account Page Test
# -------------------
def test_account_access(client, test_user):
    """
        Logs in and accesses the account page.
        Confirms the page is reachable and contains "Account".

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
            test_user: pytest fixture that provides a simulated user for testing your Flask app.
    """
    client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    response = client.get('/account')
    assert response.status_code == 200
    assert b'Account' in response.data

# -------------------
# Password Reset Request Test
# -------------------

def test_reset_request_get(client):
    """
        Tests loading the password reset form.
        Confirms HTTP 200 and the presence of "Reset Password" in the page.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
    """
    response = client.get('/reset_password')
    assert response.status_code == 200
    assert b'Reset Password' in response.data


# mock sending email
@patch('flask_blog.users.routes.send_reset_email')  # Patch where it's used, not defined
def test_reset_request_post(mock_send_email, client, test_user):
    """
        Tests loading the password reset form.
        Confirms HTTP 200 and the presence of "Reset Password" in the page.

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
            test_user: pytest fixture that provides a simulated user for testing your Flask app.
            mock_send_email: A mock object automatically passed in by @patch(...).
                             It replaces the actual send_reset_email function during the test.
    """
    response = client.post('/reset_password', data={
        'email': 'test@example.com'
    }, follow_redirects=True)

    # Check that the email function was called once with the correct user
    mock_send_email.assert_called_once_with(test_user)
    assert b'An email has been sent' in response.data

# -------------------
# User Posts Test
# -------------------
def test_user_posts(client, test_user):
    """
        Visits a user's public posts page.
        Verifies that the page loads successfully and contains the phrase "Posts by".

        Args:
            client: pytest fixture that provides a simulated browser (HTTP client) for testing your Flask app.
            test_user: pytest fixture that provides a simulated user for testing your Flask app.
    """
    response = client.get(f'/user/{test_user.username}')
    assert response.status_code == 200
    assert b'Posts by' in response.data
