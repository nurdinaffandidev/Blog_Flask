from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_blog.models import User


class RegistrationForm(FlaskForm):
    """
       Form for new user registration.

       Fields:
           - username: Required. 2–20 characters.
           - email: Required. Must be a valid email format.
           - password: Required. 6–20 characters.
           - confirm_password: Must match password.
           - submit: Sign-up button.

       Custom Validators:
           - validate_username: Ensures username is unique.
           - validate_email: Ensures email is unique.
   """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
        Form for existing user login.

        Fields:
            - email: Required. Must be a valid email format.
            - password: Required.
            - remember: Optional "Remember Me" checkbox.
            - submit: Login button.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    """
        Form for updating user account details.

        Fields:
            - username: Required. 2–20 characters.
            - email: Required. Must be a valid email format.
            - picture: Optional profile picture upload (jpg, jpeg, png).
            - submit: Update button.

        Custom Validators:
            - validate_username: Ensures updated username is unique if changed.
            - validate_email: Ensures updated email is unique if changed.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    """
       Form to request a password reset via email.

       Fields:
           - email: Required. Must be a valid email format.
           - submit: Request reset button.

       Custom Validators:
           - validate_email: Checks if the email is registered.
   """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email is not registered. Please register first.')


class ResetPasswordForm(FlaskForm):
    """
        Form to reset a user's password using a token.

        Fields:
            - password: Required. 6–20 characters.
            - confirm_password: Must match password.
            - submit: Reset password button.
    """
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')