import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"

HEADERS = {
    "Content-Type": "application/json",
}

def send_message(user_id, text):
    event = {
        "events": [{
            "type": "message",
            "replyToken": "dummy_reply_token",
            "source": {
                "userId": user_id,
                "type": "user"
            },
            "message": {
                "type": "text",
                "text": text
            }
        }]
    }

    response = requests.post(f"{BASE_URL}/callback",
                             headers=HEADERS,
                             data=json.dumps(event))

    if response.status_code == 200:
        print(f"成功發送消息: '{text}'")
        print("伺服器響應:", response.text)
    else:
        print(f"發送失敗。狀態碼: {response.status_code}")
        print("錯誤信息:", response.text)

def main():
    user_id = "test_user_001"

    while True:
        message = input("請輸入要發送的消息（輸入 'quit' 退出）: ")
        if message.lower() == 'quit':
            break
        send_message(user_id, message)

if __name__ == "__main__":
    main()