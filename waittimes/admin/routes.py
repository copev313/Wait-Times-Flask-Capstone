from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from waittimes.admin.forms import (AdminCreateUserForm, AdminDeleteUserForm,
                                   AdminUpdateUserForm)
from waittimes.models import Ride, User


admin = Blueprint('admin', __name__)


# Users Management Page
@admin.route('/manage-users', methods=['GET', 'POST'])
@login_required
def manage_users():
    # User is not an admin:
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))
    # User is an admin:
    else:
        all_users = User.query.all()
        return render_template('admin/manage_users.html', users=all_users)


# Update User Account Page:
@admin.route('/update-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    # User is not an admin:
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))

    # User is an admin:
    user = User.query.get_or_404(user_id)
    form = AdminUpdateUserForm()
    made_changes = False

    # POST -- Update Form is validated and submitted:
    if form.validate_on_submit():
        # Username is changed:
        if form.username.data not in [user.username, '']:
            username = user.username
            user.username = form.username.data
            made_changes = True
            flash(f"-Username changed from '{username}' to '{user.username}'.",
                    'success')
        # Email is changed:
        if form.email.data not in [user.email, '']:
            email = user.email
            user.email = form.email.data
            made_changes = True
            flash(f"-Email changed from '{email}' to '{user.email}'.",
                    'success')
        # Admin status is changed:
        if form.admin.data != user.is_admin:
            admin = user.is_admin
            user.is_admin = form.admin.data
            made_changes = True
            flash(f"-Admin rights changed from {admin} to {user.is_admin}.",
                    'success')
        # If changes are made update the user:
        if made_changes:
            user.save_changes()
        else:
            flash('No changes were made.', 'info')
        return redirect(url_for('admin.update_user', user_id=user.id))

    delete_form = AdminDeleteUserForm()
    # POST -- Delete Form is submitted:
    if delete_form.validate_on_submit():
        # Email matches the user to be deleted:
        if delete_form.email.data == user.email:
            # Delete the user:
            user.delete_user_account()
            return redirect(url_for('admin.manage_users'))
        else:
            flash('Email does not match the user to be deleted.', 'warning')
            return redirect(url_for('admin.update_user', user_id=user.id))

    # GET -- Populate the form with the user data:
    form.admin.data = user.is_admin
    return render_template('admin/user_edit.html',
                           form=form,
                           user=user,
                           delete_form=delete_form)


# Create User Account Page:
@admin.route('/create-user', methods=['GET', 'POST'])
@login_required
def create_user():
    # User is not an admin:
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))

    # User is an admin:
    form = AdminCreateUserForm()
    
    # POST -- Form is validated and submitted:
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        new_user.is_admin = form.admin.data
        new_user.create_user_account()
        return redirect(url_for('admin.manage_users'))
    
    # GET request:
    return render_template('admin/user_create.html', form=form)



# Delete User Account Page:
@admin.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # User is not an admin:
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))

    # User is an admin:
    user = User.query.get_or_404(user_id)
    if not user.is_admin:
        #user.delete_user_account()
        pass
    return redirect(url_for('auth.manage_users'))

