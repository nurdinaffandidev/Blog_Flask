from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

### Configurations: ###
# Configure secret key:
# Secret key will protect against modifying cookies and cross-site request forgery (csrf) attacks
app.config['SECRET_KEY'] = '7f27bc7be8123abfc4ad055db736e8aa'
# Configure database:
# Using SQLite as easiest to set up and will simply be a file on our file system
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# create database instance
db = SQLAlchemy(app)

# Models:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User(username: '{self.username}',email: '{self.email}',image_file: '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post(title: '{self.title}',date_posted: '{self.date_posted}')"

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
        flash(f'Account created for {form.username.data.title()}!', 'success') # flash: to send a one-time alert
        return redirect(url_for('index'))
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

# __name__ = main when we run script with python directly in CLI(command-line interface)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)