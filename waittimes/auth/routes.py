from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from waittimes.models import User
from werkzeug.urls import url_parse


auth = Blueprint('auth', __name__)


# REDIRECT TO LOGIN PAGE:
@auth.route('/', methods=['GET'])
def login_redirect():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


# Login Screen:
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # [CASE] The current_user is logged in:
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # [CASE] POST request:
    if (request.method == 'POST'):
        user = User.query.filter_by(email=request.form['email']).first()

        # [CASE] Incorrect email / password:
        if not user or not user.check_password(request.form['password']):
            flash("Invalid Account Credentials!")
            return redirect(url_for('auth.login'))
        
        # [CASE] User Authenticated:
        login_user(user, remember=request.form['remember'])
        current_user.set_last_login()
        next_page = request.args.get('next')
        if not next_page or (url_parse(next_page).netloc != ''):
            next_page = url_for('main.dashboard')
        return redirect(next_page)

    return render_template('auth/login.html')


# Registration Screen:
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # [CASE] The current_user is logged in:
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # [CASE] POST request:
    if (request.method == 'POST'):
        # [CASE] Confirm password DOES NOT match password:
        if (request.form['password'] != request.form['password-confirm']):
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('auth.register'))

        # Create User and add to DB:
        user = User(username=request.form['username'],
                    email=request.form['email'], 
                    password=request.form['password'])
        user.create_user_account()

        # Login User:
        login_user(user)
        current_user.set_last_login()
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/register.html')


# Logout User:
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))