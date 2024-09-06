import json
from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction

class Evaluator:
    def __init__(self, user_id: str):
        with open('questions.json', 'r') as f:
            self.questions = json.load(f)
        self.user_id = user_id
        self._init = False

    def reset(self):
        self._init = True
        self._completed = False
        self.answer = {}
        self.question_list = list(self.questions.keys())
        self.current_question_index = 0

    def is_init(self):
        return self._init

    def get_next_question(self):
        if self.is_completed():
            return self.get_result()

        question = self.question_list[self.current_question_index]
        options = self.questions[question]
        buttons = [MessageAction(label=f"{key}: {value}", text=key) for key, value in options.items()]
        return TemplateSendMessage(
            alt_text="問題",
            template=ButtonsTemplate(
                title="請回答以下問題",
                text=question,
                actions=buttons
            )
        )

    def answer_question(self, answer: str):
        if self.is_completed():
            return self.get_result()

        current_question = self.question_list[self.current_question_index]
        if answer not in self.questions[current_question]:
            return TextSendMessage(text="無效的輸入，請選擇 1, 2, 3, 或 4")

        self.answer[current_question] = answer
        self.current_question_index += 1

        return self.get_next_question()

    def is_completed(self):
        return len(self.answer) == len(self.questions)

    def get_result(self):
        level = self.evaluate()
        return TextSendMessage(text=f"評估完成！您的羽球分級評估為: {level} 級。此結果僅供參考。")

    def evaluate(self):
        scores = [int(answer) for answer in self.data.values()]
        total_score = sum(scores)

        if scores[0] == 1:  # 如果完全不了解規則和禮儀
            return 1

        if total_score <= 15:
            return 1  # 新手階1級
        elif total_score <= 20:
            return 2  # 新手階2級
        elif total_score <= 25:
            return 3  # 新手階3級
        elif total_score <= 30:
            return 4  # 初階1級
        elif total_score <= 35:
            return 5  # 初階2級
        elif total_score <= 40:
            if scores[5] >= 3 and scores[6] >= 3:  # 檢查輪轉和進攻球路
                return 6  # 初中階1級
            else:
                return 5  # 仍為初階2級
        elif total_score <= 45:
            if scores[5] >= 3 and scores[6] >= 3 and scores[7] >= 3:  # 檢查輪轉、進攻球路和防守
                return 7  # 初中階2級
            else:
                return 6  # 初中階1級
        elif total_score <= 50:
            if all(score >= 3 for score in scores[5:]):  # 檢查後五個問題是否都至少選3
                return 8  # 中階1級
            else:
                return 7  # 初中階2級
        elif total_score <= 55:
            if all(score >= 3 for score in scores[5:]) and scores[8] >= 4:  # 戰術運用至少選4
                return 9  # 中階2級
            else:
                return 8  # 中階1級
        elif total_score <= 60:
            if all(score >= 4 for score in scores[5:]):  # 後五個問題都至少選4
                return 10  # 中進階1級
            else:
                return 9  # 中階2級
        elif total_score <= 65:
            if all(score >= 4 for score in scores[5:]) and scores[9] == 4:  # 步法移動選4
                return 11  # 中進階2級
            else:
                return 10  # 中進階1級
        elif total_score <= 70:
            return 12  # 中進階3級
        else:
            return 13  # 高階或以上

    def __str__(self):
        msg = f"User ID: {self.user_id}\n"
        for index, question in enumerate(self.questions):
            msg += f"問題 {index + 1}: {question}\n"
            for key, value in self.questions[question].items():
                msg += f"  {key}: {value}\n"
            if question in self.answer:
                msg += f"回答: {self.answer[question]}\n"
            msg += "\n"

        if self.is_completed():
            level = self.evaluate()
            msg += f"評估結果: {level} 級\n"
        else:
            remaining = len(self.questions) - len(self.answer)
            msg += f"還有 {remaining} 題未回答\n"

        return msg
