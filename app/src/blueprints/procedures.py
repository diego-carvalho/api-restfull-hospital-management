# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

procedures_blueprint = Blueprint('procedures', __name__)

@procedures_blueprint.route("/procedures/", methods=['GET'])
@procedures_blueprint.route("/procedures/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM procedures")
        procedures = cursor.fetchall()
        cursor.close()

        if len(procedures) > 0:
            for procedure in procedures:

                res[procedure[0]] = {
                    'type': procedure[1],
                    'date' : procedure[2],
                    'local_id' : procedure[3],
                    'patient_id' : procedure[4]
                }
    else:
        cursor.execute("SELECT * FROM procedures WHERE id = %d" % id)
        procedure = cursor.fetchone()
        cursor.close()

        if not procedure:
            abort(404)
        res = {
            'type': procedure[1],
            'date' : procedure[2],
            'local_id' : procedure[3],
            'patient_id' : procedure[4]
        }
    return print_json(res)

@procedures_blueprint.route("/procedures/", methods=['POST'])
def post():
    type = request.form.get('type')
    d = request.form.get('date')
    local_id = request.form.get('local_id')
    patient_id = request.form.get('patient_id')

    date = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO procedures (type, date, local_id, patient_id) VALUES ('%s', '%s', %d, %d)" % (type, "{:%Y-%m-%d %H:%M:%S}".format(date), int(local_id), int(patient_id)))
        res = {cursor.lastrowid: {
            'type': type,
            'date' : "{:%Y-%m-%d H:m:s}".format(date),
            'local_id' : local_id,
            'patient_id' : patient_id
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add procedures!'}
    cursor.close()

    return print_json(res)

@procedures_blueprint.route("/procedures/<int:id>", methods=['PUT'])
def put(id):
    type = request.form.get('type')
    d = request.form.get('date')

    date = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE procedures SET type='%s', date='%s' WHERE id = %d" % (type, "{:%Y-%m-%d %H:%M:%S}".format(date), id))
        res = {id: {
            'type': type,
            'date' : "{:%Y-%m-%d H:m:s}".format(date)
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change procedures values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@procedures_blueprint.route("/procedures/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        procedure = get(id)
        cursor.execute("DELETE FROM procedures WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return procedure
    except:
        res = {'response': 'Error in change procedures values with id = %d!' % id}
        cursor.close()
        return print_json(res)