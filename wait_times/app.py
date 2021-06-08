#from dotenv import get_dotenv
from flask import Flask, render_template

#import os


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret-box'
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///waittimes_database.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
