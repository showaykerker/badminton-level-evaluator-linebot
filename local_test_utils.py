class FakeSource:
    def __init__(self, user_id):
        self.user_id = user_id
        self.type = "user"

class FakeMessage:
    def __init__(self, text):
        self.text = text
        self.type = "text"

class FakeEvent:
    def __init__(self, user_id, msg_text):
        self.source = FakeSource(user_id)
        self.message = FakeMessage(msg_text)
        self.replyToken = "dummy_reply_token"