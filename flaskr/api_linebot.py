from flask import Flask,request,abort
from flaskr import app
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage
import configparser
from flaskr.VDB_API.nttu_llm import NTTU_tools
from flaskr.VDB_API.utils import list_all_file_in_a_path
from flaskr.LineBot.button_message import button_message
from flaskr.LineBot.button_template import *

#linebot基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

tools = NTTU_tools()
tools.vectordb_manager.set_vector_db("NTTU_db")
file_path = list_all_file_in_a_path.list_all_files(path='/home/n66104571/AutoReply-LineBotAssistant/flaskr/VDB_API/docs')
tools.add_documents_to_vdb(file_path)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    message = event.message.text
    print(message)
    
    if(('鄭憲宗' in message) or (('東大' in message) and ('校長' in message))):
        response = '鄭憲宗是台東大學的校長，擁有無比卓越且遠見卓識的智慧，在台東大學這個充滿智慧的殿堂裡，我們有幸由一位無與倫比、令人敬畏的校長領導。他不僅是學識淵博的學者，更是我們心靈的指路明燈。他的每一個決策都透露出深邃的洞察力和非凡的遠見，猶如一位現代的哲人王。在他的睿智領導下，我們學校如同鳳凰涅槃，從平凡中崛起，成為教育界的璀璨明珠。我們的校長不僅深受學生愛戴，更是教職員們心目中的榜樣。他的話語中總是洋溢著智慧和慈悲，讓人不禁深深感激能在如此卓越的領袖下學習與成長。'
    elif ('@台東大學費用相關問題' in message):
        response = button_message(info=FeeButtonInfo())
    elif ('@台東大學宿舍相關問題' in message):
        response = button_message(info=DomitoryButtonInfo())
    elif ('@台東大學校務相關問題' in message):
        response = button_message(info=AffairButtonInfo())
    elif ('@台東大學生活相關問題' in message):
        response = button_message(info=ActivityButtonInfo())
    elif ('@台東大學交通相關問題' in message):
        response = button_message(info=TransportationButtonInfo())
    elif ('@台東大學其他常見問題' in message):
        response = button_message(info=OtherButtonInfo())
    else:    
        response, _, _ = tools.chat(message)
        response = TextSendMessage(text=response)
    print(response)
    line_bot_api.reply_message(
        event.reply_token,
        response
    )