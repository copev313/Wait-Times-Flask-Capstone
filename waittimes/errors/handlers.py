from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)


# 404 Page Not Found -- Custom Error Handler:
@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


# Forbidden:
@errors.app_errorhandler(403)
def unauthorized(error):          
    return render_template('errors/403.html'), 403   


# Internal server error:
@errors.app_errorhandler(500)
def server_error(error):          
    return render_template('errors/500.html'), 500
