from flask import render_template, url_for, flash, redirect
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post

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
    form = LoginForm()
    if form.validate_on_submit():
        # mock successful login
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Logged in for account {form.email.data}', 'success') # flash: to send a one-time alert
            return redirect(url_for('index'))
        else:
            flash(f'Invalid login credentials', 'danger')  # flash: to send a one-time alert
    return render_template('login.html', title="Flask Blog - Login", form=form)
