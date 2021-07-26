from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from waittimes.models import User
from waittimes.main.forms import UpdateAccountForm


main = Blueprint('main', __name__)


# Main Dashboard Screen:
@main.route('/dashboard')
@login_required
def dashboard(user='Mysterious Stranger'):
    users_name = current_user.username or user
    return render_template('main/dashboard.html', username=users_name)


# Update Account Settings Page:
@main.route('/profile/settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    msg = "No Changes Saved"
    form = UpdateAccountForm()

    # Forms submitted:
    if form.validate_on_submit():
        # If the username is changed, save changes:
        if (form.username.data != current_user.username):
            current_user.username = form.username.data
            msg = "Update Successful!"

        # If the email is changed, save changes:
        if (form.email.data != current_user.email):
            current_user.email = form.email.data
            msg = "Update Successful!"
        
        # If the password is changed, save changes:
        if (form.password.data != ""):
            current_user.set_password = form.password.data
            msg = "Update Successful!"

        # Flash confirmation message:
        flash(msg, 'success')
        if (msg.startswith("Update")):
            current_user.save_changes()

        return redirect(url_for('main.account_settings'))

    # GET request / fill form with current user info:
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('main/account_settings.html', form=form)
