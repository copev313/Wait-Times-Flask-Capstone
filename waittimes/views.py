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
from waittimes import app
from .models import User


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


''' * * * PROTECTED VIEWS * * * '''

# Main Dashboard Screen:
@app.route('/admin/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# RIDES -->  Rides Dashboard:
@app.route('/admin/rides/dashboard')
@login_required
def ride_dashboard():
    return render_template('ride_dashboard.html')

# RIDES -->  Change Ride Stats:
# RIDES -->  Create Ride:
# RIDES -->  Maintenence Records:

# WAIT TIMES -->  Summary Report:
# WAIT TIMES -->  Edit Times:
# WAIT TIMES -->  Displays:

# TICKETS --> Create Ticket:
# TICKETS --> Edit Ticket:
# TICKETS --> Ticket Records:


# PROFILE --> Account Settings:
@app.route('/admin/profile/settings')
@login_required
def account_settings():
    return render_template('account_settings.html')


# PROFILE --> Logout [Redirect to Login Screen]
@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



