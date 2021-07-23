from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required
from werkzeug.urls import url_parse
from waittimes.models import User


main = Blueprint('main', __name__)


# Main Dashboard Screen:
@main.route('/dashboard')
@login_required
def dashboard(user='Mysterious Stranger'):
    users_name = current_user.username or user
    return render_template('main/dashboard.html', username=users_name)


# PROFILE --> Account Settings:
@main.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    user = current_user
    msg = ""

    # [CASE] POST request:
    if (request.method == 'POST'):
        # Updating Username:
        if request.form['username']:
            user.username = request.form['username']
            msg = "Update Successful!"

        # Updating Email Address:
        if request.form['email']:
            user.email = request.form['email']
            msg = "Update Successful!"

        # Updating Password:
        if request.form['password']:
            # [CASE] Confirm password DOES NOT match password:
            if (request.form['password'] != request.form['password-confirm']):
                flash("Passwords do not match. Please try again.", 'error')
                return redirect(url_for('main.account_settings'))

            user.set_password(request.form['password'])
            msg = "Update Successful!"

        # Despite the name, this actually updates the User's info.
        user.create_user_account()

        # Handle Update Message:
        if msg:
            flash(msg, 'success')

        return redirect(url_for('main.account_settings'))

    else:
        return render_template('main/account_settings.html')
