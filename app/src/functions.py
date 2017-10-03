# coding: utf-8

from flask import json, Response

def print_json(obj):
    json_string = json.dumps(obj, ensure_ascii = False)
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response