# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

students_blueprint = Blueprint('students', __name__)

@students_blueprint.route("/students/", methods=['GET'])
@students_blueprint.route("/students/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()

        if len(students) > 0:
            for student in students:
                res[student[0]] = {
                    'institution' : student[1],
                    'period' : student[2],
                    'user_id' : student[3],
                }
    else:
        cursor.execute("SELECT * FROM students WHERE id = %d" % id)
        student = cursor.fetchone()
        cursor.close()

        if not student:
            abort(404)
        res = {
            'institution' : student[1],
            'period' : student[2],
            'user_id' : student[3],
        }
    return print_json(res)

@students_blueprint.route("/students/", methods=['POST'])
def post():
    institution = request.form.get('institution')
    period = request.form.get('period')
    user_id = request.form.get('user_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (institution, period, user_id) VALUES ('%s', %d, %d)" % (institution, int(period), int(user_id)))
        res = {cursor.lastrowid: {
            'institution' : institution,
            'period' : period,
            'user_id' : user_id,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add a student!'}
    cursor.close()

    return print_json(res)

@students_blueprint.route("/students/<int:id>", methods=['PUT'])
def put(id):
    institution = request.form.get('institution')
    period = request.form.get('period')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE students SET institution='%s', period=%d WHERE id = %d" % (institution, int(period), id))
        res = {id: {
            'institution' : institution,
            'period' : period,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change student values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@students_blueprint.route("/students/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        student = get(id)
        cursor.execute("DELETE FROM students WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return student
    except:
        res = {'response': 'Error in change nurstudentse values with id = %d!' % id}
        cursor.close()
        return print_json(res)