from flask import request, jsonify, abort
from flaskr import app

@app.route('/')
def hello():
    return "Hello world"