# coding: utf-8

from flask import Blueprint, request

from src.functions import print_json

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route("/users")
def index():
    peoples = [{"nome": "Bruno Rocha"},
               {"nome": "Arjen Lucassen"},
               {"nome": "Anneke van Giersbergen"},
               {"nome": "Criança muito á â "},
               {"nome": "Steven acéntõ"}]

    return print_json(peoples)