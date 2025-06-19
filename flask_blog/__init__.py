from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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
# configure Bcrypt
bcrypt = Bcrypt(app)
# configure Login Manager
login_manager = LoginManager(app)

from flask_blog import routes