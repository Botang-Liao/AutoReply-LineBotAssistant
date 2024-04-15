import inspect
from datetime import timedelta
from typing import Union
from flask import session
from flask import request, jsonify, abort
from flask.wrappers import Response
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.datastructures import FileStorage
from flaskr.user import *
from flaskr import app
#from flaskr.models import User, UserVerificationCode
from flaskr.utils import *
from flask_cors import CORS, cross_origin

URL_PREFIX: str = '/api/auth/'

# 確認 email
@app.route(URL_PREFIX + 'check-email', methods=['GET'])
def auth_check_email():
    email: str = request.args.get('email', '')
    
    if isEmpty(email) or check_email_exist(email=email):
        return jsonify(valid=False)

    return jsonify(valid=True)

# 登入
@app.route(URL_PREFIX + 'login', methods=['POST'])
@cross_origin()
def auth_login():
    data: dict = request.get_json()
    user_info: list = check_email(data['email'])
    if (user_info==[]) or (not check_password(user_info[0]['password_hash'], data['password'])):
        abort(401)
    user = User(user_info[0]['uid'])
    
    login_user(user)
    response = jsonify(success=user_info[0]['uid'])
    #response.set_cookie('session', 'session_id', httponly=False)
    return response, 200

# 登出
@app.route(URL_PREFIX + 'logout', methods=['POST'])
#@login_required
def auth_logout():
    logout_user()
    return jsonify(success=True), 200

# 註冊
@app.route(URL_PREFIX + 'signup', methods=['POST'])
def auth_sign_up():
    data: dict = request.get_json()
    if isEmpty(data['email'], data['username'], data['password']):
        abort(400)
    if check_email_exist(email=data['email']):
        abort(403)
    
    sql = 'INSERT INTO User (email, username, password_hash, verified, score, last_edit) VALUES (?, ?, ?, ?, ?, ?);'
    param = (data['email'], data['username'], generate_password_hash(data['password']), 0, 5, datetime_now_to_integer())
    db.engine.execute(sql, param)
    return jsonify(success=True), 200


