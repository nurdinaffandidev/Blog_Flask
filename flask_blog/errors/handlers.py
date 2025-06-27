from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_not_found(error):
    """
        Handle 404 Not Found errors.

        Args:
            error (Exception): The raised 404 error.

        Returns:
            Response: Rendered '404.html' template with 404 status code.
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_forbidden(error):
    """
        Handle 403 Forbidden errors.

        Args:
            error (Exception): The raised 403 error.

        Returns:
            Response: Rendered '403.html' template with 403 status code.
    """
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_internal_server(error):
    """
        Handle 500 Internal Server errors.

        Args:
            error (Exception): The raised 500 error.

        Returns:
            Response: Rendered '500.html' template with 500 status code.
    """
    return render_template('errors/500.html'), 500