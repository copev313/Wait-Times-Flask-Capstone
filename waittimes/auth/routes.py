from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from waittimes.auth.forms import RegistrationForm, LoginForm
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
    # Current_user is already logged in:
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    # Form is submitted:
    if form.validate_on_submit():
        # Check if user exists:
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('auth.login'))

        # User is authenticated:
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)

    # GET request:
    return render_template('auth/login.html', form=form)


# Registration Screen:
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Current_user is already logged in:
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    # Form is submitted:
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        # Creates the new user and saves it to the database:
        user.create_user_account()
        # Login User:
        login_user(user)
        current_user.set_last_login()
        # Redirect to the dashboard:
        return redirect(url_for('main.dashboard'))
    
    # GET request:
    return render_template('auth/register.html', form=form)


# Logout User:
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
