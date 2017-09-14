# coding: utf-8


from flask import Blueprint, request
from src import mysql

from src.functions import print_json

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route("/users/", methods=['GET'])
@users_blueprint.route("/users/<int:id>", methods=['GET'])
def get(id=None):
    if not id:
        peoples = [{"nome": "Bruno Rocha"},
               {"nome": "Arjen Lucassen"},
               {"nome": "Anneke van Giersbergen"},
               {"nome": "Criança muito á â "},
               {"nome": "Steven acéntõ"}]
        return print_json(peoples)
    else:
        conn = mysql.connect()
        return "User " + str(id)

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
def edit(id=None):
    return "Edit User " + str(id)

"""
product_view = ProductView.as_view('product_view')
app.add_url_rule(
    '/product/', view_func=product_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/product/<int:id>', view_func=product_view, methods=['GET', 'PUT', 'DELETE']
)


import sys

from flask import request, jsonify, Blueprint, abort
from my_app import mysql
from flask.views import MethodView

# print(products, file=sys.stderr)

class ProductView(MethodView):
    def get(self, id=None):
        if not id:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product")
            products = cursor.fetchall()
            cursor.close()

            res = {}
            
            if len(products) > 0:
                for product in products:
                    res[product[0]] = {
                        'name': product[1],
                        'price': product[2]
                    }
            
        else:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product WHERE id = %d" % id)
            product = cursor.fetchone()
            cursor.close()

            if not product:
                abort(404)
            res = {
                'name': product[1],
                'price': product[2]
            }
            print(res, file=sys.stderr)
        return jsonify(res)

    def post(self):
        name = request.form.get('name')
        price = request.form.get('price')

        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO product(name, price) VALUES ('%s', %s)" % (name, price))
            res = {cursor.lastrowid: {
                'name': name,
                'price': price,
            }}
            conn.commit()
        except:
            res = {'response': 'Error in create user!'}
        cursor.close()

        return jsonify(res)

    def put(self, id):
        name = request.form.get('name')
        price = request.form.get('price')
        conn = mysql.connect()
        cursor = conn.cursor()
        # print("UPDATE product SET name='%s', price=%s WHERE id=%d" % (name, price, id), file=sys.stderr)
        try:
            cursor.execute(
                "UPDATE product SET name='%s', price=%s WHERE id=%d" % (name, price, id))
            res = {id: {
                'name': name,
                'price': price,
            }}
            conn.commit()
        except:
            res = {'response': 'Error in change user values with id = %d!' % id}
        cursor.close()
        return jsonify(res)
 
    def delete(self, id):
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM product WHERE id=%d" % id)
            res = {'response': 'Object is been remove with id = %d!' % id}
            conn.commit()
        except:
            res = {'response': 'Error in change user values with id = %d!' % id}
        cursor.close()
        return jsonify(res)"""