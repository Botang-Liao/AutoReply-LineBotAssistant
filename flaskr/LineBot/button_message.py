from linebot.models import *
from flaskr.LineBot.button_template import ButtonTemplateInfo 

def button_message(info: ButtonTemplateInfo):
    message = TemplateSendMessage(
        alt_text=' This is a ButtonsTemplate',
        template= ButtonsTemplate(
            thumbnail_image_url=info.url,
            title=info.title,
            text=info.text,
            actions=[MessageTemplateAction(label=keyword, text=question) for keyword, question in zip(info.keywords, info.questions)]
        )
    )

    return message