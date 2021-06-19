from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)
from werkzeug.urls import url_parse
from waittimes import app, db
from .models import User, Ride


# 404 Page Not Found -- Custom Error Handler:
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Login Screen
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # [CASE] The current_user is logged in:
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # [CASE] POST request:
    if (request.method == 'POST'):
        user = User.query.filter_by(email=request.form['email']).first()

        # [CASE] Incorrect email / password:
        if not user or not user.check_password(request.form['password']):
            flash("Invalid Account Credentials!")
            return redirect(url_for('login'))
        
        # [CASE] User Authenticated:
        login_user(user, remember=request.form['remember'])
        current_user.set_last_login()
        next_page = request.args.get('next')
        if not next_page or (url_parse(next_page).netloc != ''):
            next_page = url_for('dashboard')
        return redirect(next_page)

    return render_template('login.html')


# Registration Screen:
@app.route('/register', methods=['GET', 'POST'])
def register():
    # [CASE] The current_user is logged in:
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # [CASE] POST request:
    if (request.method == 'POST'):
        # [CASE] Confirm password DOES NOT match password:
        if (request.form['password'] != request.form['password-confirm']):
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))

        # Create User and add to DB:
        user = User(username=request.form['username'],
                    email=request.form['email'], 
                    password=request.form['password'])
        user.create_user_account()

        # Login User:
        login_user(user)
        current_user.set_last_login()
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


''' * * * * * * PROTECTED VIEWS * * * * * * '''

# Main Dashboard Screen:
@app.route('/admin/dashboard')
@login_required
def dashboard(user='Mysterious Stranger'):
    users_name = current_user.username or user
    return render_template('dashboard.html', username=users_name)


# RIDES -->  Rides Dashboard:
@app.route('/admin/rides/dashboard')
@login_required
def ride_dashboard(rides_list=[]):
    rides_list = Ride.query.all() or rides_list
    return render_template('ride_dashboard.html', rides=rides_list)


# RIDES -->  Change Ride Info:
@app.route('/admin/rides/edit')
@login_required
def edit_ride_info():
    return render_template('change_ride_info.html')


# RIDES -->  Create Ride:
@app.route('/admin/rides/create', methods=['GET', 'POST'])
@login_required
def create_ride():
    # [CASE] POST request:
    if (request.method == 'POST'):
        ride_name = request.form['name']
        ride = None

        if request.form['waittime']:
            ride_wt = request.form['waittime']
            ride = Ride(ride_name, ride_wt)
        else:
            ride = Ride(ride_name)

        if request.form['status']:
            ride_status = request.form['status']
            ride.set_ride_status(ride_status)
        
        if request.form['imagelink']:
            ride_img = request.form['imagelink']
            ride.set_ride_image(ride_img)

        if request.form['notes']:
            ride_notes = request.form['notes']
            ride.write_optional_notes(ride_notes)

        ride.create_ride()
        return redirect(url_for('create_ride'))

    return render_template('create_a_ride.html')



# WAIT TIMES -->  Summary Report:
@app.route('/admin/waittimes/summary')
@login_required
def wait_summary():
    rides_list = Ride.query.all()
    return render_template('wt_summary.html', rides=rides_list)


# WAIT TIMES -->  Edit Times:
@app.route('/admin/waittimes/edit')
@login_required
def wait_edit(rides_list=[]):
    rides_list = Ride.query.all() or rides_list
    return render_template('wt_edit.html', rides=rides_list)


# TICKETS --> Create Ticket:
@app.route('/admin/tickets/create')
@login_required
def create_ticket():
    return render_template('create_ticket.html')

# TICKETS --> Edit Ticket:
@app.route('/admin/tickets/edit')
@login_required
def edit_ticket():
    return render_template('edit_ticket.html')


# TICKETS --> Ticket Records:
@app.route('/admin/tickets/records')
@login_required
def ticket_records():
    return render_template('ticket_records.html')


# PROFILE --> Account Settings:
@app.route('/admin/profile/settings', methods=['GET', 'POST'])
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
                flash("Passwords do not match. Please try again.")
                return redirect(url_for('account_settings'))

            user.set_password(request.form['password'])
            msg = "Update Successful!"

        # Despite the name, this actually updates the User's info.
        user.create_user_account()

        # Handle Update Message:
        if msg:
            flash(msg)

        return redirect(url_for('account_settings'))

    else:
        return render_template('account_settings.html')


# PROFILE --> Admin Mode Login:
@app.route('/admin/profile/admin-mode-login', methods=['GET', 'POST'])
@login_required
def admin_mode_login():
    return render_template('admin_mode_login.html')


# PROFILE --> Admin Panel:
@app.route('/admin/profile/admin-panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html')


# PROFILE --> Logout [Redirect to Login Screen]
@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
