import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from messages import more_info, level_table_url

if os.environ.get('ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

USER_DATA = {}

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
def handle_message(event):

    message = TextSendMessage(text=event.message.text)

    if event.source.type != "user":
        app.logger.info(f"Source type is not user: {event.source}")
        return

    try:
        user_id = event.source.user_id
        app.logger.info(f"Get user_id from event.source: {user_id}")
    except:
        app.logger.error(f"Can not get user_id from event.source: {event.source}")
        return

    if user_id not in USER_DATA:
        USER_DATA[user_id] = {}
    if event.message.text == "開始測試":
        message = TextSendMessage(text=USER_DATA[user_id])
    elif event.message.text == "更多資訊":
        message = TextSendMessage(text=more_info)
    elif event.message.text == "分級表":
        # send image "level_table.jpg"
        message = ImageSendMessage(
            original_content_url=level_table_url,
            preview_image_url=level_table_url
        )
    else:
        message = TextSendMessage(text=f"Got message: {event.message.text}")
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)