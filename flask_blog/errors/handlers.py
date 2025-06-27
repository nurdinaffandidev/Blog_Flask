from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_not_found(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_forbidden(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_internal_server(error):
    return render_template('errors/500.html'), 500