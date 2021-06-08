#from dotenv import get_dotenv
from flask import Flask, render_template

#import os


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret-box'
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///waittimes_database.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Home Screen (for tests):
@app.route('/')
def index():
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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
