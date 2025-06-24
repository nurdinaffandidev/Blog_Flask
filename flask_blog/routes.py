from flask import render_template, url_for, flash, redirect
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Mock posts
posts = [
    {
        'author': 'Nurdin Affandi',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Jun 17, 2025'
    },
    {
        'author': 'Joshi Boy',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Jun 18, 2025'
    }
]

# Routes:
@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="Flask Blog - About")

@app.route("/register", methods=['GET', 'POST'])
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

@app.route("/login", methods=['GET', 'POST']) # name of route
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
            flash(f'Logged in for account {form.email.data}', 'success')  # flash: to send a one-time alert
            return redirect(url_for('index'))
        else:
            flash(f'Invalid login credentials', 'danger')  # flash: to send a one-time alert
    return render_template('login.html', title="Flask Blog - Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')