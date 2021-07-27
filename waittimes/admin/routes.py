from flask import Blueprint,redirect, render_template, url_for
from flask_login import current_user, login_required
from waittimes.models import User


admin = Blueprint('admin', __name__)


# Users Management Page
@admin.route('/manage-users', methods=['GET', 'POST'])
@login_required
def manage_users():
    # User is an admin:
    if current_user.is_admin:
        all_users = User.query.all()
        return render_template('admin/manage_users.html', users=all_users)
    # User is not an admin:
    return redirect(url_for('main.dashboard'))




@admin.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # User is an admin:
    if current_user.is_admin:
        user = User.query.get_or_404(user_id)
        # Temporary:
        return redirect(url_for('main.dashboard'))
        # TODO: Delete user from database + save changes:
    # User is not an admin:
    return redirect(url_for('main.dashboard'))
    
    