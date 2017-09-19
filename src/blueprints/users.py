# coding: utf-8

import sys

from flask import Blueprint, request
from src import mysql

from src.functions import print_json

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route("/users/", methods=['GET'])
@users_blueprint.route("/users/<int:id>", methods=['GET'])
def get(id=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    res = {}
    if not id:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()

        if len(users) > 0:
            for user in users:
                res[user[0]] = {
                    'name': user[1]
                }
    else:
        cursor.execute("SELECT * FROM users WHERE id = %d" % id)
        user = cursor.fetchone()
        cursor.close()

        if not user:
            abort(404)
        res = {
            'name': user[1]
        }
    return print_json(res)

@users_blueprint.route("/users/", methods=['POST'])
def post():
    name = request.form.get('name')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name) VALUES ('%s')" % name)
        res = {cursor.lastrowid: {
            'name': name,
        }}
        conn.commit()
    except:
        res = {'response': 'Error in add user!'}
    cursor.close()

    return print_json(res)

@users_blueprint.route("/users/<int:id>", methods=['PUT'])
def put(id):
    name = request.form.get('name')

    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET name='%s' WHERE id=%d" % (name, id))
        res = {id: {
            'name': name
        }}
        conn.commit()
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
    cursor.close()
    
    return print_json(res)

@users_blueprint.route("/users/<int:id>", methods=['DELETE'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        user = get(id)
        cursor.execute("DELETE FROM users WHERE id=%d" % id)
        conn.commit()
        cursor.close()
        return user
    except:
        res = {'response': 'Error in change user values with id = %d!' % id}
        cursor.close()
        return print_json(res)