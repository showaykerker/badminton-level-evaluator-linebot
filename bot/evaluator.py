import json
from linebot.v3.messaging import (
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    MessageAction
)

class Evaluator:
    def __init__(self, user_id: str):
        possible_questions_path = ['questions.json', 'bot/questions.json']
        for path in possible_questions_path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.questionnaire = json.load(f)
                break
            except FileNotFoundError:
                pass
        else:
            app.logger.error("quesions.json not found")
            raise FileNotFoundError("questions.json not found")
        self.user_id = user_id
        self._init = False
        self._completed = False
        self.current_question_id = None
        self.answers = {}

    def reset(self):
        self._init = True
        self._completed = False
        self.answers = {}
        self.current_question_id = 1  # 從第一個問題開始

    def is_init(self):
        return self._init

    def valid_answer(self, answer: str):
        try:
            current_options = self.questionnaire['questions'][self.current_question_id - 1]['options']
            return any(answer == option['text'] for option in current_options)
        except TypeError:
            return False

    def get_next_question(self):
        if self.is_completed():
            return self.get_result()

        question = next((q for q in self.questionnaire['questions'] if q['id'] == self.current_question_id), None)
        if not question:
            self._completed = True
            return self.get_result()

        options = question['options']
        buttons = [
            MessageAction(
                label=option['text'][:20],  # Label 最多 20 個字
                text=options[i]['text']
            ) for i, option in enumerate(options)
        ]
        return TemplateMessage(
            alt_text="問題",
            template=ButtonsTemplate(
                title=f"請回答以下問題 ({question['id']}/{len(self.questionnaire['questions'])})",
                text=question['text'],
                actions=buttons[:4]  # Line Bot 限制最多 4 個按鈕
            )
        )

    def answer_question(self, answer: str):

        if self.is_completed():
            return self.get_result()

        question = next((q for q in self.questionnaire['questions'] if q['id'] == self.current_question_id), None)
        if not question:
            return TextMessage(text="問題不存在")

        # the answer is now the text of the option selected, not the index
        # option = question['options'][int(answer) - 1]
        option = next((o for o in question['options'] if o['text'] == answer), None)
        self.answers[self.current_question_id] = option

        if 'result' in option:
            self._completed = True
            return self.get_result()
        elif 'next' in option:
            self.current_question_id = option['next']
        else:
            self._completed = True

        return self.get_next_question()

    def is_completed(self):
        return self._completed

    def get_result(self):
        level = self.evaluate()
        return TextMessage(text=f"評估完成！\n您的羽球分級評估為: {level}。\n此結果僅供參考。")

    def debug(self):
        if not self.is_completed():
            return "尚未完成評估"
        msg = f"User ID: {self.user_id}\n"
        msg += "="*20 + "\n"
        for q_id, answer in self.answers.items():
            msg += f"{q_id} | {answer['text']}\n"
        msg += "="*20 + "\n"
        msg += f"評估結果: {self.evaluate()}\n"
        return msg

    def evaluate(self):
        if not self.is_completed():
            return "尚未完成評估"

        for q_id, answer in self.answers.items():
            if 'result' in answer:
                return self.questionnaire['results'][str(answer['result'])]

        return "無法確定級別"

    def __str__(self):
        msg = f"User ID: {self.user_id}\n"
        for question in self.questionnaire['questions']:
            msg += f"問題 {question['id']}: {question['text']}\n"
            for option in question['options']:
                msg += f"  {option['text']}\n"
            if question['id'] in self.answers:
                msg += f"回答: {self.answers[question['id']]['text']}\n"
            msg += "\n"

        if self.is_completed():
            level = self.evaluate()
            msg += f"評估結果: {level}\n"
        else:
            msg += "評估尚未完成\n"

        return msg

if __name__ == "__main__":
    from messages import more_info, image_url
    evaluator = Evaluator("test_user")
    options = []
    while True:
        user_msg = input("輸入訊息：")
        print("\n")
        if user_msg in ["1", "2", "3", "4"]:
            user_msg = int(user_msg)
            user_msg = options[user_msg-1]

        if user_msg in ["開始測試", "重新開始", "a"]:
            evaluator.reset()
            response_msg = evaluator.get_next_question()
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
        elif user_msg == "q":
            print(evaluator)
            break
        else:
            print(f"Unknown message: {user_msg}")

        options = []
        if isinstance(response_msg, TextMessage):
            print(response_msg.text)
        elif response_msg.template:
            print(response_msg.template.title)
            print(response_msg.template.text)
            for i, action in enumerate(response_msg.template.actions):
                options.append(action.text)
                print(f"\t{i+1}. {action.label}")