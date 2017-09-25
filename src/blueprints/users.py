# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

from src.blueprints.phones import getAllByUser as phone_get
from src.blueprints.address import getAllByUser as address_get

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route("/users/", methods=['GET'])
@users_blueprint.route("/users/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()

        if len(users) > 0:
            for user in users:
                phones = phone_get(int(user[0]))
                address = address_get(int(user[0]))

                res[user[0]] = {
                    'name': user[3],
                    'cpf' : user[4],
                    'email' : user[5],
                    'birthdate' : user[6],
                    'admin' : user[7],
                    'doctor' : user[8],
                    'nurse' : user[9],
                    'student' : user[10],
                    'patient' : user[11],
                    'council_president' : user[12],
                    'phones' : phones,
                    'addres' : address
                }
    else:
        cursor.execute("SELECT * FROM users WHERE id = %d" % id)
        user = cursor.fetchone()
        cursor.close()

        if not user:
            abort(404)
        res = {
            'name': user[3],
            'cpf' : user[4],
            'email' : user[5],
            'birthdate' : user[6],
            'admin' : user[7],
            'doctor' : user[8],
            'nurse' : user[9],
            'student' : user[10],
            'patient' : user[11],
            'council_president' : user[12]
        }
    return print_json(res)

@users_blueprint.route("/users/", methods=['POST'])
def post():
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    birthdate = request.form.get('birthdate')
    admin = request.form.get('admin')
    doctor = request.form.get('doctor')
    nurse = request.form.get('nurse')
    student = request.form.get('student')
    patient = request.form.get('patient')
    council = request.form.get('council_president')

    date = datetime.strptime(birthdate, "%Y-%m-%d")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (login, password, name, cpf, email, birthday, admin, doctor, nurse, student, patient, council_president) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, %d)" % (login, password, name, cpf, email, "{:%Y-%m-%d}".format(date), int(admin), int(doctor), int(nurse), int(student), int(patient), int(council)))
        res = {cursor.lastrowid: {
            'name': name,
            'cpf' : cpf,
            'email' : email,
            'birthdate' : birthdate,
            'admin' : admin,
            'doctor' : doctor,
            'nurse' : nurse,
            'student' : student,
            'patient' : patient,
            'council_president' : council
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add user!'}
    cursor.close()

    return print_json(res)

@users_blueprint.route("/users/<int:id>", methods=['PUT'])
def put(id):
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    birthdate = request.form.get('birthdate')
    admin = request.form.get('admin')
    doctor = request.form.get('doctor')
    nurse = request.form.get('nurse')
    student = request.form.get('student')
    patient = request.form.get('patient')
    council = request.form.get('council_president')

    date = datetime.strptime(birthdate, "%Y-%m-%d")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET login='%s', password='%s', name='%s', cpf='%s', email='%s', birthday='%s', admin=%d, doctor=%d, nurse=%d, student=%d, patient=%d, council_president=%d WHERE id = %d" % (login, password, name, cpf, email, "{:%Y-%m-%d}".format(date), int(admin), int(doctor), int(nurse), int(student), int(patient), int(council), id))
        res = {id: {
            'name': name,
            'cpf' : cpf,
            'email' : email,
            'birthdate' : birthdate,
            'admin' : admin,
            'doctor' : doctor,
            'nurse' : nurse,
            'student' : student,
            'patient' : patient,
            'council_president' : council
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@users_blueprint.route("/users/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        user = get(id)
        cursor.execute("DELETE FROM users WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return user
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
        cursor.close()
        return print_json(res)