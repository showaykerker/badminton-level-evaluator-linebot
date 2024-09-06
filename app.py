import os
import json

from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from messages import more_info, level_table_url
from evaluator import Evaluator

if os.environ.get('ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

EVALUATORS = {}

@app.route("/callback", methods=['POST'])
def callback():
    if os.environ.get('ENV') == 'local':
        # 在本地環境中，直接處理請求體
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        handle_local_request(body)
        return 'OK'
    else:
        # 在非本地環境中，使用正常的簽名驗證流程
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)
        return 'OK'

def handle_local_request(body):
    body_json = json.loads(body)
    for event in body_json['events']:
        if event['type'] == 'message':
            if event['message']['type'] == 'text':
                handle_message(event)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    if event['source']['type'] != "user":
        app.logger.info(f"Source type is not user: {event['source']}")
        return

    try:
        app.logger.info(f"Get user_id from event.source: {event['source']['userId']}")
    except:
        app.logger.error(f"Can not get user_id from event.source: {event['source']}")
        return

    user_id = event['source']['userId']

    if user_id not in EVALUATORS:
        EVALUATORS[user_id] = Evaluator(user_id)

    evaluator = EVALUATORS[user_id]

    if event['message']['text'] in ["開始測試", "重新開始"]:
        evaluator.reset()
        message = evaluator.get_next_question()
    elif event['message']['text'] == "更多資訊":
        message = TextMessage(text=more_info)
    elif event['message']['text'] == "分級表":
        message = ImageMessage(
            original_content_url=level_table_url,
            preview_image_url=level_table_url
        )
    elif event['message']['text'] in ["1", "2", "3", "4"] and evaluator.is_init():
        message = evaluator.answer_question(event['message']['text'])
    elif not evaluator.is_init():
        message = TextMessage(text="請輸入「開始測試」來開始評估")
    else:
        # message = TextMessage(text="請回答 1, 2, 3, 4 或「重新開始」")
        app.logger.info(f"Unknown message: {event['message']['text']}")
        if os.environ.get('ENV') == 'local':
            print(f"Unknown message: {event['message']['text']}")
        return

    if os.environ.get('ENV') == 'local':
        try:
            print(f"Would send message: {message.text}")
        except AttributeError:
            print(f"Would send message: {message}")
    else:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event['replyToken'],
                    messages=[message]
                )
            )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)