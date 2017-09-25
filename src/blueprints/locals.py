# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

locals_blueprint = Blueprint('locals', __name__)

@locals_blueprint.route("/locals/", methods=['GET'])
@locals_blueprint.route("/locals/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM local")
        locals = cursor.fetchall()
        cursor.close()

        if len(locals) > 0:
            for local in locals:
                res[local[0]] = {
                    'block' : local[1],
                    'number' : local[2],
                    'type' : local[3],
                }
    else:
        cursor.execute("SELECT * FROM local WHERE id = %d" % id)
        local = cursor.fetchone()
        cursor.close()

        if not local:
            abort(404)
        res = {
            'block' : local[1],
            'number' : local[2],
            'type' : local[3],
        }
    return print_json(res)

@locals_blueprint.route("/locals/", methods=['POST'])
def post():
    block = request.form.get('block')
    number = request.form.get('number')
    type = request.form.get('type')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO local (block, number, type) VALUES ('%s', '%s', '%s')" % (block, number, type))
        res = {cursor.lastrowid: {
            'block' : block,
            'number' : number,
            'type' : type,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add a local!'}
    cursor.close()

    return print_json(res)

@locals_blueprint.route("/locals/<int:id>", methods=['PUT'])
def put(id):
    block = request.form.get('block')
    number = request.form.get('number')
    type = request.form.get('type')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE local SET block='%s', number='%s', type='%s' WHERE id = %d" % (block, number, type, id))
        res = {id: {
            'block' : block,
            'number' : number,
            'type' : type,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change local values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@locals_blueprint.route("/locals/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        local = get(id)
        cursor.execute("DELETE FROM local WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return local
    except:
        res = {'response': 'Error in change locals values with id = %d!' % id}
        cursor.close()
        return print_json(res)