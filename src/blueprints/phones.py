# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

phones_blueprint = Blueprint('phones', __name__)

def getAllByUser(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    cursor.execute("SELECT * FROM phones WHERE user_id = %d" % user_id)
    phones = cursor.fetchall()
    cursor.close()
    if len(phones) > 0:
        for phone in phones:
            res[phone[0]] = {
                'phone': phone[1],
            }
    return res

@phones_blueprint.route("/phones/", methods=['GET'])
@phones_blueprint.route("/phones/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM phones")
        phones = cursor.fetchall()
        cursor.close()

        if len(phones) > 0:
            for phone in phones:
                res[phone[0]] = {
                    'phone': phone[1],
                    'user_id' : phone[2]
                }
    else:
        
        cursor.execute("SELECT * FROM phones WHERE id = %d" % id)
        phone = cursor.fetchone()
        cursor.close()
        
        if not phone:
            abort(404)
        res = {
            'phone': phone[1],
            'user_id' : phone[2]
        }
    return print_json(res)

@phones_blueprint.route("/phones/", methods=['POST'])
def post():
    phone = request.form.get('phone')
    user_id = request.form.get('user_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO phones (phone, user_id) VALUES ('%s', %d)" % (phone, int(user_id)))
        res = {cursor.lastrowid: {
            'phone': phone,
            'user_id' : user_id
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add user!'}
    cursor.close()

    return print_json(res)

@phones_blueprint.route("/phones/<int:id>", methods=['PUT'])
def put(id):
    phone = request.form.get('phone')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE phones SET phone='%s' WHERE id = %d" % (phone, id))
        res = {id: {
            'phone': phone
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@phones_blueprint.route("/phones/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        phone = get(id)
        cursor.execute("DELETE FROM phones WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return phone
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
        cursor.close()
        return print_json(res)