from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return "index"


@app.route('/home')
def home():
    return 'home'


@app.route('/home/<string:username>')
def user_page(variable_name):
    variable_name = escape(variable_name)
    return f"{variable_name}"


with app.test_request_context():
