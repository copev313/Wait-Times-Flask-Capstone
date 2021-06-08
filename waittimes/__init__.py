'''https://pythonise.com/series/learning-flask/flask-application-structure'''

from flask import Flask


app = Flask(__name__)


from waittimes import views

app.run(debug=True)