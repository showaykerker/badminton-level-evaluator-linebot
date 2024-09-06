import json
from linebot.v3.messaging import (
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    Action
)

class Evaluator:
    def __init__(self, user_id: str):
        with open('questions.json', 'r') as f:
            self.questions = json.load(f)
        self.user_id = user_id
        self._init = False
        self._completed = False

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
        buttons = [Action(label=f"{key}: {value}", text=key) for key, value in options.items()]
        return TemplateMessage(
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

        # 如果完全不了解規則和禮儀，則直接跳過後面所有問題，complete 設為 True
        if self.current_question_index == 0 and answer == "1":
            self.answer[self.question_list[0]] = 1
            self.current_question_index = len(self.question_list) - 1
            self._completed = True
            return self.get_result()

        current_question = self.question_list[self.current_question_index]
        if answer not in self.questions[current_question]:
            return TextMessage(text="無效的輸入，請選擇 1, 2, 3, 或 4")

        self.answer[current_question] = answer
        self.current_question_index += 1

        return self.get_next_question()

    def is_completed(self):
        return self._completed or len(self.answer) == len(self.questions)

    def get_result(self):
        level = self.evaluate()
        return TextMessage(text=f"評估完成！您的羽球分級評估為: {level} 級。此結果僅供參考。")

    def debug(self):
        if not self.is_completed():
            return "尚未完成評估"
        msg = f"User ID: {self.user_id}\n"
        msg += "="*20 + "\n"
        for key, value in self.answer.items():
            msg += f"{value} | {key}\n"
        msg += "="*20 + "\n"
        msg += f"評估結果: {self.evaluate()} 級\n"
        msg += f"score: {self._get_score()[1]}\n\n"
        return msg

    def _get_score(self):
        scores = [int(answer) for answer in self.answer.values()]
        total_score = sum(scores)
        return scores, total_score

    def evaluate(self):
        scores, total_score = self._get_score()

        if scores[0] == 1:  # 如果完全不了解規則和禮儀
            return 1

        if total_score == 10:
            return 1  # 新手階1級
        elif total_score <= 15:
            return 2  # 新手階2級
        elif total_score <= 20:
            return 3  # 新手階3級
        elif total_score <= 34:
            return 4  # 初階1級
        elif total_score <= 30:
            if scores[5] >= 3 and scores[6] >= 3:  # 檢查輪轉和進攻球路
                return 6  # 初中階1級
            else:
                return 5  # 初階2級
        elif total_score <= 35:
            if scores[5] >= 3 and scores[6] >= 3 and scores[7] >= 3:  # 檢查輪轉、進攻球路和防守
                return 7  # 初中階2級
            elif all(score >= 3 for score in scores[5:]):  # 檢查後五個問題是否都至少選3
                return 8  # 中階1級
            else:
                return 6  # 初中階1級
        else:
            if all(score >= 4 for score in scores[5:]):  # 後五個問題都至少選4
                return 13  # 高階或以上
            elif all(score >= 3 for score in scores[5:]) and scores[8] >= 4:  # 戰術運用至少選4
                return 10  # 中進階1級
            elif all(score >= 3 for score in scores[5:]):
                return 9  # 中階2級
            else:
                return 8  # 中階1級

    def __str__(self):
        msg = f"User ID: {self.user_id}\n"
        for index, question in enumerate(self.questions):
            if not question in self.answer: break
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

def main():
    print("歡迎使用羽球程度評估系統！")
    evaluator = Evaluator("local_user")

    while True:
        command = input("請輸入指令 (開始測試/重新開始/結束程式): ")
        if command == "結束程式":
            print("感謝使用，再見！")
            break
        elif command in ["開始測試", "重新開始", ""]:
            evaluator.reset()
            while not evaluator.is_completed():
                question = evaluator.get_next_question()
                if isinstance(question, TemplateSendMessage):
                    print(f"\n{question.template.text}")
                    for action in question.template.actions:
                        print(f"{action.text}: {action.label.split(': ')[1]}")
                elif isinstance(question, TextMessage):
                    print(question.text)
                    break

                answer = input("請輸入您的答案 (1-4): ")
                result = evaluator.answer_question(answer)
                if isinstance(result, TextMessage):
                    print(result.text)

            print("\n詳細問卷:")
            print(evaluator)
        elif command in ["debug", "d"]:
            print(evaluator.debug())
        else:
            print("無效的指令，請重新輸入。")

if __name__ == "__main__":
    main()