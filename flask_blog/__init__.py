from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config

### Configurations: ###
# create database instance
db = SQLAlchemy()
# configure Bcrypt
bcrypt = Bcrypt()
# configure Login Manager
login_manager = LoginManager()
# configure login view of login_manager
login_manager.login_view = 'users.login' # 'login' => function name of route
login_manager.login_message_category = 'info'
mail = Mail()

# defining creation of app into a function to allow creation of different instances of application with different configurations
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import blueprints instances
    from flask_blog.users.routes import users
    from flask_blog.posts.routes import posts
    from flask_blog.main.routes import main

    # register blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
