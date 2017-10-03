# coding: utf-8

import sys

from datetime import datetime
from flask import Blueprint, request

from src import mysql
from src.functions import print_json

address_blueprint = Blueprint('address', __name__)

def getAllByUser(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    cursor.execute("SELECT * FROM address WHERE user_id = %d" % user_id)
    address = cursor.fetchall()
    cursor.close()
    if len(address) > 0:
        for adr in address:
            res[adr[0]] = {
                'cep': adr[1],
                'state' : adr[2],
                'city' : adr[3],
                'neighborhood' : adr[4],
                'street' : adr[5],
                'number' : adr[6],
            }
    return res

@address_blueprint.route("/address/", methods=['GET'])
@address_blueprint.route("/address/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM address")
        address = cursor.fetchall()
        cursor.close()

        if len(address) > 0:
            for adr in address:
                res[adr[0]] = {
                    'cep': adr[1],
                    'state' : adr[2],
                    'city' : adr[3],
                    'neighborhood' : adr[4],
                    'street' : adr[5],
                    'number' : adr[6],
                    'user_id' : adr[7],
                }
    else:
        cursor.execute("SELECT * FROM address WHERE id = %d" % id)
        adr = cursor.fetchone()
        cursor.close()

        if not adr:
            abort(404)
        res = {
            'cep': adr[1],
            'state' : adr[2],
            'city' : adr[3],
            'neighborhood' : adr[4],
            'street' : adr[5],
            'number' : adr[6],
            'user_id' : adr[7],
        }
    return print_json(res)

@address_blueprint.route("/address/", methods=['POST'])
def post():
    cep = request.form.get('cpf')
    state = request.form.get('state')
    city = request.form.get('city')
    neighborhood = request.form.get('neighborhood')
    street = request.form.get('street')
    number = request.form.get('number')
    user_id = request.form.get('user_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO address (cep, state, city, neighborhood, street, number, user_id) VALUES ('%s', '%s', '%s', '%s', '%s', %d, %d)" % (cep, state, city, neighborhood, street, int(number), int(user_id)))
        res = {cursor.lastrowid: {
            'cep': cep,
            'state' : state,
            'city' : city,
            'neighborhood' : neighborhood,
            'street' : street,
            'number' : number,
            'user_id' : user_id,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add user!'}
    cursor.close()

    return print_json(res)

@address_blueprint.route("/address/<int:id>", methods=['PUT'])
def put(id):
    cep = request.form.get('cep')
    state = request.form.get('state')
    city = request.form.get('city')
    neighborhood = request.form.get('neighborhood')
    street = request.form.get('street')
    number = request.form.get('number')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE address SET cep='%s', state='%s', city='%s', neighborhood='%s', street='%s', number=%d WHERE id = %d" % (cep, state, city, neighborhood, street, int(number), id))
        res = {id: {
            'cep': cep,
            'state' : state,
            'city' : city,
            'neighborhood' : neighborhood,
            'street' : street,
            'number' : number,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@address_blueprint.route("/address/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        adr = get(id)
        cursor.execute("DELETE FROM address WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return adr
    except:
        res = {'response': 'Error in change adr values with id = %d!' % id}
        cursor.close()
        return print_json(res)