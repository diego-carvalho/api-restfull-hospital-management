# coding: utf-8

import sys

from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'api-hospital'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

from src.blueprints.users import users_blueprint
app.register_blueprint(users_blueprint)

from src.blueprints.phones import phones_blueprint
app.register_blueprint(phones_blueprint)

from src.blueprints.address import address_blueprint
app.register_blueprint(address_blueprint)

from src.blueprints.doctors import doctors_blueprint
app.register_blueprint(doctors_blueprint)

from src.blueprints.nurses import nurses_blueprint
app.register_blueprint(nurses_blueprint)

from src.blueprints.students import students_blueprint
app.register_blueprint(students_blueprint)

from src.blueprints.locals import locals_blueprint
app.register_blueprint(locals_blueprint)

from src.blueprints.historys import historys_blueprint
app.register_blueprint(historys_blueprint)

@app.route("/")
@app.route('/home/')
def home():
    return 'Welcome to the api v1 of Santa Rocha da Misericórdia hospital'