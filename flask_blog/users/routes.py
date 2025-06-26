from flask import Blueprint

# create instance of Blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
        return redirect(url_for('login'))
    return render_template('register.html', title="Flask Blog - Register", form=form)


@users.route("/login", methods=['GET', 'POST']) # name of route
def login(): # name of function
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid login credentials', 'danger')  # flash: to send a one-time alert
    return render_template('login.html', title="Flask Blog - Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
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
        return redirect(url_for('account')) # redirect required due to post-get-redirect pattern
    elif request.method == 'GET': # populate fields with current_user data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
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
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title="Request Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # check existing logged in user
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # get hashed password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # set new password
        user.password = hashed_password
        db.session.commit()
        # show feedback
        flash(f'Password successfully reset for {user.email}! You are able to login with your new password!', 'success') # flash: to send a one-time alert
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password", form=form)