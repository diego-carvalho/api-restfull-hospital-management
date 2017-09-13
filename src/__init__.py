# coding: utf-8

import sys

from flask import Flask

from src.functions import print_json


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Welcome in my aplication"