# coding: utf-8

import sys

from flask import Flask

from src.blueprints.users import users_blueprint


app = Flask(__name__)

app.register_blueprint(users_blueprint)

@app.route("/")
def hello_world():
    return "Welcome in my aplication"