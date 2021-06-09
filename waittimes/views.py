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


# Main Route [Redirect to Login Screen]:
@app.route('/')
def main():
    return redirect(url_for('login'))


# Login Screen
@app.route('/login', methods=['GET', 'POST'])
def login():
    # [CASE] The current_user is logged in:
    if current_user.is_authenticated:
        username = current_user.username or 'Mysterious_Stranger'
        return redirect(url_for('dashboard', username=username))

    # [CASE] POST request:
    if (request.method == 'POST'):
        user = User.query.filter_by(email=request.form['email']).first()

        # [CASE] Incorrect email / password:
        if not user or not user.check_password(request.form['password']):
            flash("Invalid Account Credentials!", category='error')
            return redirect(url_for('login'))
        
        # [CASE] User Authenticated:
        login_user(user, remember=request.form['remember'])
        user.set_last_login()
        next_page = request.args.get('next')
        if not next_page or (url_parse(next_page).netloc != ''):
            next_page = url_for('dashboard', username=user.username)
            flash("Login Successful!", category='info')
        return redirect(next_page)

    return render_template('login.html')


# Registration Screen:
@app.route('/register', methods=['GET', 'POST'])
def register():
    # [CASE] The current_user is logged in:
    if current_user.is_authenticated:
        username = current_user.username or 'Mysterious_Stranger'
        return redirect(url_for('dashboard', username=username))
    
    # [CASE] POST request:
    if (request.method == 'POST'):
        # TODO: Fill me in!
        return redirect(url_for('register.html'))
    
    return render_template('register.html')


# Logout Route [Redirect to Login Screen]
def logout():
    logout_user()
    return redirect(url_for('login'))


# Dashboard Screen [protected]:
@app.route('/admin/dashboard/<username>')
@login_required
def dashboard(username):
    username = 'Hashy'
    return render_template('dashboard.html', username=username)


# Ride Data Screen [protected]:
@app.route('/admin/ride/<name>')
def ride(name):
    username = 'Hashy'
    #name = 'RIDE NAME'
    return render_template('ride.html', username=username, ride_name=name)
