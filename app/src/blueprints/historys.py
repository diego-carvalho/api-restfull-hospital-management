# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

historys_blueprint = Blueprint('historys', __name__)

@historys_blueprint.route("/historys/", methods=['GET'])
@historys_blueprint.route("/historys/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM history")
        historys = cursor.fetchall()
        cursor.close()

        if len(historys) > 0:
            for history in historys:
                res[history[0]] = {
                    'date': history[1],
                    'disease' : history[2],
                    'treatment' : history[3],
                    'result' : history[4],
                    'observation' : history[5],
                    'user_id' : history[6],
                }
    else:
        cursor.execute("SELECT * FROM history WHERE id = %d" % id)
        history = cursor.fetchone()
        cursor.close()

        if not history:
            abort(404)
        res = {
            'date': history[1],
            'disease' : history[2],
            'treatment' : history[3],
            'result' : history[4],
            'observation' : history[5],
            'user_id' : history[6],
        }
    return print_json(res)

@historys_blueprint.route("/historys/", methods=['POST'])
def post():
    d = request.form.get('date')
    disease = request.form.get('disease')
    treatment = request.form.get('treatment')
    result = request.form.get('result')
    observation = request.form.get('observation')
    user_id = request.form.get('user_id')

    date = datetime.strptime(d, "%Y-%m-%d")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO history (date, disease, treatment, result, observation, user_id) VALUES ('%s', '%s', '%s', '%s', '%s', %d)" % ("{:%Y-%m-%d}".format(date), disease, treatment, result, observation, int(user_id)))
        res = {cursor.lastrowid: {
            'date': date,
            'disease' : disease,
            'treatment' : treatment,
            'result' : result,
            'observation' : observation,
            'user_id' : user_id,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add history!'}
    cursor.close()

    return print_json(res)

@historys_blueprint.route("/historys/<int:id>", methods=['PUT'])
def put(id):
    d = request.form.get('date')
    disease = request.form.get('disease')
    treatment = request.form.get('treatment')
    result = request.form.get('result')
    observation = request.form.get('observation')
    user_id = request.form.get('user_id')

    date = datetime.strptime(d, "%Y-%m-%d")

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE history SET date='%s', disease='%s', treatment='%s', result='%s', observation='%s', user_id=%d WHERE id = %d" % ("{:%Y-%m-%d}".format(date), disease, treatment, result, observation, int(user_id), id))
        res = {id: {
            'date': date,
            'disease' : disease,
            'treatment' : treatment,
            'result' : result,
            'observation' : observation,
            'user_id' : user_id,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change history values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@historys_blueprint.route("/historys/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        history = get(id)
        cursor.execute("DELETE FROM history WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return history
    except:
        res = {'response': 'Error in change history values with id = %d!' % id}
        cursor.close()
        return print_json(res)