from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email


# create instance of Blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
        Handle user registration.

        - Redirects authenticated users to the main index page.
        - Displays a registration form for new users.
        - Validates form submission and creates a new user account with a hashed password.
        - Commits the user to the database and flashes a success message upon successful registration.
        - Redirects the user to the login page after registration.

        Returns:
            Response: Rendered registration template on GET or failed POST.
                      Redirect to login page on successful registration.
    """
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # get hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # creating user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # adding user to db
        db.session.add(user)
        db.session.commit()
        # show feedback
        flash(f'Account created for {form.username.data.title()}! You are able to login with your new account!', 'success') # flash: to send a one-time alert
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Flask Blog - Register", form=form)


@users.route("/login", methods=['GET', 'POST']) # name of route
def login(): # name of function
    """
        Handle user login.

        - Redirects authenticated users to the home page.
        - Processes login form submission.
        - Authenticates user using email and password.
        - Redirects to the originally requested page if specified (`next` parameter).
        - Flashes success or error messages.

        Returns:
            Response: Renders login page or redirects to the appropriate page after login.
    """
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # check if user exists in database
        user = User.query.filter_by(email=form.email.data).first()
        # check password matches in database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # add next_page routing to where page user was trying to access but prompted for login
            # sample url: http://localhost:5001/login?next=%2Faccount
            next_page = request.args.get('next')
            flash(f'Logged in for account {form.email.data}', 'success')  # flash: to send a one-time alert
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid login credentials', 'danger')  # flash: to send a one-time alert
    return render_template('login.html', title="Flask Blog - Login", form=form)


@users.route("/logout")
def logout():
    """
        Logs out the current user and redirects to the main index page.

        Returns:
            Response: Redirect to home page.
    """
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
        Display and update the current user's account information.

        - Allows users to update their username, email, and profile picture.
        - Pre-populates the form with current values on GET request.
        - Commits changes on POST and redirects to avoid form resubmission.

        Returns:
            Response: Renders the account page or redirects after successful update.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # update username and email via current_user and commiting to db
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')  # flash: to send a one-time alert
        return redirect(url_for('users.account')) # redirect required due to post-get-redirect pattern
    elif request.method == 'GET': # populate fields with current_user data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    """
       Display blog posts by a specific user.

       Args:
           username (str): Username of the user whose posts are being viewed.

       Returns:
           Response: Renders a paginated list of blog posts by the user.
   """
    page = request.args.get('page', 1, type=int)
    # getting user from username
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query\
            .filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
        Handle password reset request.

        - Prevents logged-in users from accessing.
        - Sends a password reset email if the provided email is registered.

        Returns:
            Response: Renders password reset request page or redirects after sending email.
    """
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title="Request Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
        Handle password reset using a secure token.

        - Verifies the token and identifies the user.
        - Allows user to set a new password if the token is valid.
        - Flashes feedback messages on success or failure.

        Args:
            token (str): Secure token used to verify password reset request.

        Returns:
            Response: Renders reset password form or redirects on failure/success.
    """
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # get hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # set new password
        user.password = hashed_password
        db.session.commit()
        # show feedback
        flash(f'Password successfully reset for {user.email}! You are able to login with your new password!', 'success') # flash: to send a one-time alert
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)