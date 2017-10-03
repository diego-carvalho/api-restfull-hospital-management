# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

doctors_blueprint = Blueprint('doctors', __name__)

@doctors_blueprint.route("/doctors/", methods=['GET'])
@doctors_blueprint.route("/doctors/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        cursor.close()

        if len(doctors) > 0:
            for doctor in doctors:
                res[doctor[0]] = {
                    'specialty': doctor[1],
                    'registry' : doctor[2],
                    'user_id' : doctor[3],
                }
    else:
        cursor.execute("SELECT * FROM doctors WHERE id = %d" % id)
        doctor = cursor.fetchone()
        cursor.close()

        if not doctor:
            abort(404)
        res = {
            'specialty': doctor[1],
            'registry' : doctor[2],
            'user_id' : doctor[3],
        }
    return print_json(res)

@doctors_blueprint.route("/doctors/", methods=['POST'])
def post():
    specialty = request.form.get('specialty')
    registry = request.form.get('registry')
    user_id = request.form.get('user_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO doctors (specialty, registry, user_id) VALUES ('%s', '%s', %d)" % (specialty, registry, int(user_id)))
        res = {cursor.lastrowid: {
            'specialty': specialty,
            'registry' : registry,
            'user_id' : user_id,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add a doctor!'}
    cursor.close()

    return print_json(res)

@doctors_blueprint.route("/doctors/<int:id>", methods=['PUT'])
def put(id):
    specialty = request.form.get('specialty')
    registry = request.form.get('registry')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE doctors SET specialty='%s', registry='%s' WHERE id = %d" % (specialty, registry, id))
        res = {id: {
            'specialty': specialty,
            'registry' : registry,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change doctor values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@doctors_blueprint.route("/doctors/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        doctor = get(id)
        cursor.execute("DELETE FROM doctors WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return doctor
    except:
        res = {'response': 'Error in change doctor values with id = %d!' % id}
        cursor.close()
        return print_json(res)