from flask import request, jsonify, abort
from flask.wrappers import Response
from flaskr import app
from flaskr.utils import *
from flask_login import current_user, login_required
from flaskr.user import User
from typing import Any, Dict, List, Union
from werkzeug.security import generate_password_hash, check_password_hash
from transformers import BertTokenizer, BertModel
import torch

# 檢查GPU是否可用，並將模型和輸入張量移動到GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('GanymedeNil/text2vec-large-chinese')
model = BertModel.from_pretrained('GanymedeNil/text2vec-large-chinese')
#device = "cpu"
model.to(device)

app_route = '/api/user/'


@app.route('/')
def hello():
    return "Hello world"

# 得到使用者的資訊
@app.route(app_route + "get-info", methods=['GET'])
#@login_required
def user_get_info():
    # headers = request.headers
    # # 取得所有的標頭欄位
    # for header, value in headers.items():
    #     print(f'{header}: {value}')
    #data: dict = request.get_json()
    #pritn(data)
    #(str(current_user.id))
    sql = "SELECT * FROM User WHERE uid = " + str(current_user.id)
    datas = data_process(sql)
    datas[0].pop('password_hash', None)
    return jsonify(datas[0])

# 得到活動資訊
@app.route(app_route + "get-post-info", methods=['GET'])
#@login_required
def get_post_info():
    time = datetime_now_to_integer()
    param = str(request.args.get('type','0'))  
    
    sql = "SELECT pid, title, about, date, address, number_of_people_limitation, space_available, "
    sql += "content, expected_cost_lowerbound, expected_cost_upperbound FROM Post, Activity WHERE acid = activity AND date > " + str(time)
    if param != '0':
        sql += (" AND atid = " + param) 
    
    datas = data_process(sql)
    return jsonify(datas)

# 得到揪團類型資訊
@app.route(app_route + "get-activity-type-info", methods=['GET'])
#@login_required
def get_activity_type_info():
    sql = "SELECT name FROM ActivityType"
    datas = data_process_with_special_case(sql)
    return jsonify(datas)

# 得到活動資訊
@app.route(app_route + "get-activity-info", methods=['GET'])
#@login_required
def get_activity_info():
    param = str(request.args.get('type','0'))  
    sql = "SELECT name FROM Activity"
    if param != '0':
        sql += (" WHERE atid = " + param) 
    
    datas = data_process_with_special_case(sql)
    return jsonify(datas)

# 修改使用者資訊
@app.route(app_route + "set-info", methods=['POST'])
#@login_required
def set_info():
    data: dict = request.get_json()

    if isEmpty(data['email'], data['username'], data['password']):
        abort(400)

    sql = "SELECT * FROM User WHERE uid = ?;"
    datas = data_process_with_param(sql, (current_user.id))[0]
    tuples = []
    for i in data:
        if (i == 'password') and (not isEmpty(data[i])):
            tuples.append(generate_password_hash(data[i]))
        else:
            tuples.append(data[i])

    tuples.append(datetime_now_to_integer()) 
    tuples.append(current_user.id)
    sql = "UPDATE User SET email=?, username=?, password_hash=?, education=?, about=?, language=?, other_info=?, last_edit=? WHERE uid = ?"
    tuples = tuple(tuples)
    #print(tuples)
    db.engine.execute(sql, tuples)
    #print(datas)

    return jsonify(success=True), 200
    
# 新增活動
@app.route(app_route + "add-post", methods=['POST'])
@login_required
def add_post():
    headers = request.headers
    # 取得所有的標頭欄位
    for header, value in headers.items():
        print(f'{header}: {value}')
    print('='*20)
    data: dict = request.get_json()
    keys =', '.join(['uid', 'time'] + list(data.keys())) 
    params = [current_user.id, datetime_now_to_integer()] + list(data.values())
    qm = '?, ' * (len(params)-1) + '?'
    params = tuple(params) 
    
    try:
        sql = 'INSERT INTO Post (' + keys + ') VALUES (' + qm + ')'
        #sql = 'INSERT INTO Post (uid,  time, activity, title, about, date, address,number_of_people_limitation, space_available, content, latitude, longitude, expected_cost_lowerbound, expected_cost_upperbound) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        db.engine.execute(sql, params)
    except:
        abort(400)
    return jsonify(success=True), 200


# 參加活動
@app.route(app_route + "join-post", methods=['POST'])
@login_required
def join_post():
    data: dict = request.get_json()
    keys =', '.join(['uid'] + list(data.keys())) 
    params = [current_user.id] + list(data.values())
    qm = '?, ' * (len(params)-1) + '?'
    params = tuple(params) 
    
    #sql = "SELECT * FROM User WHERE uid = " + str(current_user.id)
    #datas = data_process(sql)

    try:
        sql = 'INSERT INTO Participant (' + keys + ') VALUES (' + qm + ')'
        db.engine.execute(sql, params)
        sql = 'UPDATE Post SET space_available=space_available-? WHERE pid=?'
        db.engine.execute(sql, (data['number'], data['pid']))
    except:
        abort(400)
    
    return jsonify(success=True), 200


# 推薦活動
@app.route(app_route + "recommmend-post", methods=['GET'])
@login_required
def rec_post():
    time = datetime_now_to_integer()
    param = str(request.args.get('keyword','0')) 
    sql = "SELECT pid, title, about, date, address, number_of_people_limitation, space_available, "
    sql += "content, expected_cost_lowerbound, expected_cost_upperbound, name FROM Post, Activity WHERE acid = activity AND date > " + str(time)
    datas = data_process(sql)
    tts_param = traditional_to_simplified(param)
    
    similarities = []

    for data in datas:
        string = data['name'] + ':' + data['title']
        if not isEmpty((data['about'])):
            string += '，' + data['about']
        sentences = [tts_param, traditional_to_simplified(string)]
        print(sentences)
        encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        encoded_input = {key: value.to(device) for key, value in encoded_input.items()}

        with torch.no_grad():
            # 呼叫模型的前向計算並將輸出移回CPU
            model_output = model(**encoded_input)#.to('cpu')

        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        output = cos(sentence_embeddings[0].reshape((1, 1024)), sentence_embeddings[1].reshape((1, 1024)))
        similarities.append(output.item())
    #print(similarities)
    #print(datas)
    sorted_datas = [score for _, score in sorted(zip(similarities, datas), key=lambda x: x[0], reverse=True)]
    #print(sorted_datas)
    return jsonify(sorted_datas)