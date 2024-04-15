from typing import Any
from flaskr import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import opencc
import torch
def isEmpty(*args: str) -> bool:
    """ Check if any argument in *args is an empty string. """
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


def isNone(*args: Any) -> bool:
    """ Check if any argument in *args is None. """
    for arg in args:
        if arg == None:
            return True
    return False

def data_process(sql: str) -> list:
    """ Execute SQL and make data type be list. """
    datas = []
    
    tuples = db.engine.execute(sql)
    for t in tuples:
        data = {}
        #print(t._mapping.items())
        for i,j in t._mapping.items():
            #print(i,j)
            data.setdefault(i,j)
        datas.append(data)
    return datas

def data_process_with_param(sql: str, param : tuple) -> list:
    """ Execute SQL and make datatype be a list. """
    datas = []
    #print('sql語法:', sql)
    #print('sql參數:', param)
    tuples = db.engine.execute(sql, param)
    for t in tuples:
        data = {}
        #print(t._mapping.items())
        for i,j in t._mapping.items():
            #print(i,j)
            data.setdefault(i,j)
        datas.append(data)
    return datas

# 針對只要一個 attribute 的狀況
def data_process_with_special_case(sql: str) -> list:
    tuples = db.engine.execute(sql)
    return ([i[0] for i in tuples.fetchall()])

def datetime_now_to_integer():
    time=int(datetime.now().timestamp())
    std_timestamp = int(datetime(2023,4,22).timestamp())
    return(time - std_timestamp)

def datetime_to_integer(time : datetime) -> int:
    time=int(time.timestamp())
    std_timestamp = int(datetime(2023,4,22).timestamp())
    return(time - std_timestamp)

def integer_to_datetime(integer : int) -> datetime:
    std_timestamp = int(datetime(2023, 4, 22).timestamp())
    timestamp = std_timestamp + integer
    dt = datetime.fromtimestamp(timestamp)
    return dt

def check_email_exist(email: str) -> bool:
    sql: str = 'SELECT email FROM User Where email = ' + '\"' + email + '\"'
    return(data_process(sql) != [])
    
def check_email(email: str) -> bool:
    sql: str = 'SELECT * FROM User Where email = ' + '\"' + email + '\"'
    return(data_process(sql))

def check_password(answer: str, password: str) -> bool:
    ans: bool = check_password_hash(answer, password)
    return(ans)

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def traditional_to_simplified(traditional_text):
    cc = opencc.OpenCC('t2s')  # 建立繁體字到簡體字的轉換器
    simplified_text = cc.convert(traditional_text)  # 將繁體字轉換成簡體字
    return simplified_text

def simplified_to_traditional(simplified_text):
    cc = opencc.OpenCC('s2t')  # 建立簡體字到繁體字的轉換器
    traditional_text = cc.convert(simplified_text)  # 將簡體字轉換成繁體字
    return traditional_text