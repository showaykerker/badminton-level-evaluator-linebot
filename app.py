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
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    if event.source.type != "user":
        app.logger.info(f"Source type is not user: {event.source}")
        return

    try:
        app.logger.info(f"Get user_id from event.source: {event.source.user_id}")
    except:
        app.logger.error(f"Can not get user_id from event.source: {event.source}")
        return

    user_id = event.source.user_id

    if user_id not in EVALUATORS:
        EVALUATORS[user_id] = Evaluator(user_id)

    evaluator = EVALUATORS[user_id]
    user_msg = event.message.text

    if user_msg in ["開始測試", "重新開始", "a"]:
        evaluator.reset()
        response_msg = evaluator.get_next_question()
    elif user_msg in ["debug", "d"]:
        response_msg = TextMessage(text=evaluator.debug())
    elif user_msg == "更多資訊":
        response_msg = TextMessage(text=more_info)
    elif user_msg == "分級表":
        response_msg = ImageMessage(
            original_content_url=level_table_url,
            preview_image_url=level_table_url
        )
    elif user_msg in ["1", "2", "3", "4"] and evaluator.is_init():
        response_msg = evaluator.answer_question(user_msg)
    elif not evaluator.is_init():
        response_msg = TextMessage(text="請輸入「開始測試」來開始評估")
    else:
        app.logger.info(f"Unknown message: {user_msg}")
        return

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event['replyToken'],
                messages=[response_msg]
            )
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)