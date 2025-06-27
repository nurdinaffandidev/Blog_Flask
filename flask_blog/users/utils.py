import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail
from string import Template


def save_picture(form_picture):
    """
       Randomize picture file name, resized picture and save picture file locally.

       Args:
           form_picture (FileStorage): Picture file data.

       Returns:
           str: Picture file name.
    """
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_file_name)

    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_file_name


def send_reset_email(user):
    """
        Sends a password reset email to the specified user.

        This function generates a secure token for the user and constructs a password
        reset URL. It then sends an email with this URL to the user's registered email
        address using Flask-Mail.

        Args:
            user (User): The user object for whom the password reset is requested.
                         Must have a `get_reset_token()` method and `email`, `username` attributes.

        Returns:
            None
    """
    # set token and reset_url
    token = user.get_reset_token()
    reset_url = url_for('users.reset_token', token=token, _external=True)

    # message subject line
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])

    # message body
    msg_template = Template("""
    Hi $name,

    To reset your password, visit the following link:
    $reset_link

    If you did not make this request, please ignore this email.

    Best regards,  
    Support Team
    """)

    msg.body = msg_template.substitute(name=user.username.title(), reset_link=reset_url)

    # send email
    mail.send(msg)
    return None