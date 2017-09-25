# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

nurses_blueprint = Blueprint('nurses', __name__)

@nurses_blueprint.route("/nurses/", methods=['GET'])
@nurses_blueprint.route("/nurses/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM nurses")
        nurses = cursor.fetchall()
        cursor.close()

        if len(nurses) > 0:
            for nurse in nurses:
                res[nurse[0]] = {
                    'registry' : nurse[1],
                    'user_id' : nurse[2],
                }
    else:
        cursor.execute("SELECT * FROM nurses WHERE id = %d" % id)
        nurse = cursor.fetchone()
        cursor.close()

        if not nurse:
            abort(404)
        res = {
            'registry' : nurse[1],
            'user_id' : nurse[2],
        }
    return print_json(res)

@nurses_blueprint.route("/nurses/", methods=['POST'])
def post():
    registry = request.form.get('registry')
    user_id = request.form.get('user_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO nurses (registry, user_id) VALUES ('%s', %d)" % (registry, int(user_id)))
        res = {cursor.lastrowid: {
            'registry' : registry,
            'user_id' : user_id,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add a nurse!'}
    cursor.close()

    return print_json(res)

@nurses_blueprint.route("/nurses/<int:id>", methods=['PUT'])
def put(id):
    registry = request.form.get('registry')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE nurses SET registry='%s' WHERE id = %d" % (registry, id))
        res = {id: {
            'registry' : registry,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change nurse values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@nurses_blueprint.route("/nurses/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        nurse = get(id)
        cursor.execute("DELETE FROM nurses WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return nurse
    except:
        res = {'response': 'Error in change nurse values with id = %d!' % id}
        cursor.close()
        return print_json(res)