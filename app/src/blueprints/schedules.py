# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

schedules_blueprint = Blueprint('schedules', __name__)

@schedules_blueprint.route("/schedules/", methods=['GET'])
@schedules_blueprint.route("/schedules/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM schedules")
        schedules = cursor.fetchall()
        cursor.close()

        print(schedules, file=sys.stderr)

        if len(schedules) > 0:
            for schedule in schedules:

                res[schedule[0]] = {
                    'date' : schedule[1],
                    'start_time' : str(schedule[2]),
                    'end_time' : str(schedule[3]),
                    'function' : schedule[4],
                    'procedure_id' : schedule[5],
                    'type_official' : schedule[6],
                    'official_id' : schedule[7]
                }
    else:
        cursor.execute("SELECT * FROM schedules WHERE id = %d" % id)
        schedule = cursor.fetchone()
        cursor.close()

        if not schedule:
            abort(404)
        res = {
            'date' : schedule[1],
            'start_time' : str(schedule[2]),
            'end_time' : str(schedule[3]),
            'function' : schedule[4],
            'procedure_id' : schedule[5],
            'type_official' : schedule[6],
            'official_id' : schedule[7]
        }
    return print_json(res)

@schedules_blueprint.route("/schedules/", methods=['POST'])
def post():
    d = request.form.get('date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    function = request.form.get('function')
    procedure_id = request.form.get('procedure_id')
    type_official = request.form.get('type_official')
    official_id = request.form.get('official_id')

    date = datetime.strptime(d, "%Y-%m-%d")

    print(start_time, file=sys.stderr)

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO schedules (date, start_time, end_time, function, procedure_id, type_official, official_id) VALUES ('%s', '%s', '%s', '%s', %d, %d, %d)" % ("{:%Y-%m-%d}".format(date), start_time, end_time, function, int(procedure_id), int(type_official), int(official_id)))
        res = {cursor.lastrowid: {
            'date' : "{:%Y-%m-%d}".format(date),
            'start_time' : start_time,
            'end_time' : end_time,
            'function' : function,
            'procedure_id' : procedure_id,
            'type_official' : type_official,
            'official_id' : official_id
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add schedules!'}
    cursor.close()

    return print_json(res)

@schedules_blueprint.route("/schedules/<int:id>", methods=['PUT'])
def put(id):
    d = request.form.get('date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    function = request.form.get('function')
    
    date = datetime.strptime(d, "%Y-%m-%d")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE schedules SET date='%s', start_time='%s', end_time='%s', function='%s' WHERE id = %d" % ("{:%Y-%m-%d %H:%M:%S}".format(date), str(start_time), str(end_time), function, id))
        res = {id: {
            'date' : "{:%Y-%m-%d}".format(date),
            'start_time' : start_time,
            'end_time' : end_time,
            'function' : function
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change schedules values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@schedules_blueprint.route("/schedules/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        schedule = get(id)
        cursor.execute("DELETE FROM schedules WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return schedule
    except:
        res = {'response': 'Error in change schedules values with id = %d!' % id}
        cursor.close()
        return print_json(res)