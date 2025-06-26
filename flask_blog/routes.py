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










