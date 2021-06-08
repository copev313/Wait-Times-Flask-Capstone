from flask import render_template
from waittimes import app


# Home Screen (for tests):
@app.route('/')
def home():
    return render_template('index.html')


# Login Screen:
@app.route('/login')
def login():
    return render_template('login.html')


# Registration Screen:
@app.route('/register')
def register():
    return render_template('register.html')


# Dashboard Screen [protected]:
@app.route('/dashboard')
def dashboard(username):
    username = 'Hashy'
    return render_template('dashboard.html', username=username)


# Ride Data Screen [protected]:
@app.route('/ride/<name>')
def ride(name):
    username = 'Hashy'
    name = 'RIDE NAME'
    return render_template('ride.html', username=username, ride_name=name)