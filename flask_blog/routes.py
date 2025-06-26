import secrets
import os

from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog import app, db, bcrypt, mail
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from flask_mail import Message
from string import Template


# Routes:
@app.route("/")
@app.route("/home")
def index():
    # setting default page
    page = request.args.get('page', 1, type=int)
    # setting number of post per page
    # Note: this results in posts becoming a Pagination object
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="Flask Blog - About")









