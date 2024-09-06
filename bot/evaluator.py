import json
from linebot.v3.messaging import (
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    MessageAction
)

class Evaluator:
    def __init__(self, user_id: str):
        with open('questions.json', 'r', encoding='utf-8') as f:
            self.questionnaire = json.load(f)
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
        return any(answer == option['text'] for option in self.questionnaire['questions'][self.current_question_id - 1]['options'])

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