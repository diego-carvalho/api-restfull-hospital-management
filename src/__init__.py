# coding: utf-8

import sys

from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'api-hospital'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

from src.blueprints.users import users_blueprint
app.register_blueprint(users_blueprint)

@app.route("/")
@app.route('/home/')
def home():
    return 'Welcome to the api v1 of Santa Rocha da Misericórdia hospital'