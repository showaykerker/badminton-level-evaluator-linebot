import os
import json
import time

from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessageAction,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from .messages import more_info, image_url, note, dm_guidance, usage_guidance
from ..core.evaluator import Evaluator

if os.environ.get('ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

EVALUATORS = {}

RATE_LIMIT_SECONDS = 86400  # 1 day
_non_dm_rate_limit = {}  # user_id -> last_reply_timestamp
_unknown_msg_rate_limit = {}  # user_id -> last_reply_timestamp


def _is_rate_limited(store: dict, user_id: str) -> bool:
    now = time.time()
    last_time = store.get(user_id, 0)
    if now - last_time < RATE_LIMIT_SECONDS:
        return True
    store[user_id] = now
    return False

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

def evaluate_dict_to_msg(evaluate_dict: dict):
    if evaluate_dict['is_end']:
        level = evaluate_dict['level']
        return TextMessage(text=f"評估完成！\n您的羽球分級評估為: {level}。\n此結果僅供參考。")
    else:
        assert "options" in evaluate_dict
        assert "question" in evaluate_dict
        assert "id" in evaluate_dict
        assert "total" in evaluate_dict
        buttons = [
            MessageAction(
                label=option[:20],  # Label 最多 20 個字
                text=option
            ) for option in evaluate_dict['options']
        ]
        return TemplateMessage(
            alt_text="問題",
            template=ButtonsTemplate(
                title=f"請回答以下問題 ({evaluate_dict['id']}/{evaluate_dict['total']})",
                text=evaluate_dict['question'],
                actions=buttons[:4]  # Line Bot 限制最多 4 個按鈕
            )
        )

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    if event.source.type != "user":
        app.logger.info(f"Source type is not user: {event.source}")
        source_user_id = getattr(event.source, 'user_id', None)
        if source_user_id and not _is_rate_limited(_non_dm_rate_limit, source_user_id):
            try:
                with ApiClient(configuration) as api_client:
                    line_bot_api = MessagingApi(api_client)
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=dm_guidance)]
                        )
                    )
            except Exception as e:
                app.logger.error(f"Failed to reply non-DM guidance: {e}")
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
        response_msg = evaluate_dict_to_msg(evaluator.get_next_question())
    elif user_msg in ["debug", "d"]:
        response_msg = TextMessage(text=evaluator.debug())
    elif user_msg == "更多資訊":
        response_msg = TextMessage(text=more_info)
    elif user_msg == "分級表":
        response_msg = ImageMessage(original_content_url=image_url, preview_image_url=image_url)
    elif evaluator.valid_answer(user_msg) and evaluator.is_init():
        response_msg = evaluator.answer_question(user_msg)
    elif not evaluator.is_init():
        response_msg = TextMessage(text="請輸入「開始測試」來開始評估")
    else:
        app.logger.info(f"Unknown message: {user_msg}")
        if not _is_rate_limited(_unknown_msg_rate_limit, user_id):
            response_msg = TextMessage(text=usage_guidance)
        else:
            return

    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[response_msg]
                )
            )
    except Exception as e:
        app.logger.error(f"Failed to reply message: {e}")
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="有東西壞掉了QQ，請稍後再試")]
                )
            )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)