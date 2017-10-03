# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

hospitalized_blueprint = Blueprint('hospitalized', __name__)

@hospitalized_blueprint.route("/hospitalized/", methods=['GET'])
@hospitalized_blueprint.route("/hospitalized/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM hospitalized")
        hospitalized = cursor.fetchall()
        cursor.close()

        if len(hospitalized) > 0:
            for hst in hospitalized:

                res[hst[0]] = {
                    'start_date': hst[1],
                    'end_date' : hst[2],
                    'local_id' : hst[3],
                    'patient_id' : hst[4]
                }
    else:
        cursor.execute("SELECT * FROM hospitalized WHERE id = %d" % id)
        hst = cursor.fetchone()
        cursor.close()

        if not hst:
            abort(404)
        res = {
            'start_date': hst[1],
            'end_date' : hst[2],
            'local_id' : hst[3],
            'patient_id' : hst[4]
        }
    return print_json(res)

@hospitalized_blueprint.route("/hospitalized/", methods=['POST'])
def post():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    local_id = request.form.get('local_id')
    patient_id = request.form.get('patient_id')

    s_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    e_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO hospitalized (start_date, end_date, local_id, patient_id) VALUES ('%s', '%s', %d, %d)" % ("{:%Y-%m-%d %H:%M:%S}".format(s_date), "{:%Y-%m-%d %H:%M:%S}".format(e_date), int(local_id), int(patient_id)))
        res = {cursor.lastrowid: {
            'start_date': "{:%Y-%m-%d H:m:s}".format(s_date),
            'end_date' : "{:%Y-%m-%d H:m:s}".format(e_date),
            'local_id' : local_id,
            'patient_id' : patient_id
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add hospitalized!'}
    cursor.close()

    return print_json(res)

@hospitalized_blueprint.route("/hospitalized/<int:id>", methods=['PUT'])
def put(id):
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    s_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    e_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE hospitalized SET start_date='%s', end_date='%s' WHERE id = %d" % ("{:%Y-%m-%d %H:%M:%S}".format(s_date), "{:%Y-%m-%d %H:%M:%S}".format(e_date), id))
        res = {id: {
            'start_date': "{:%Y-%m-%d H:m:s}".format(s_date),
            'end_date' : "{:%Y-%m-%d H:m:s}".format(e_date)
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change hospitalized values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@hospitalized_blueprint.route("/hospitalized/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        hst = get(id)
        cursor.execute("DELETE FROM hospitalized WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return hst
    except:
        res = {'response': 'Error in change hospitalized values with id = %d!' % id}
        cursor.close()
        return print_json(res)