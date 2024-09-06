import unittest
import json
from unittest.mock import patch, mock_open
from evaluator import Evaluator
from linebot.v3.messaging import TextMessage, TemplateMessage

mock_questions = {
    "questions": [
        {
            "id": 1,
            "text": "Question 1?",
            "options": [
                {"text": "Option 1", "next": 2},
                {"text": "Option 2", "result": 1}
            ]
        },
        {
            "id": 2,
            "text": "Question 2?",
            "options": [
                {"text": "Option 1", "result": 2},
                {"text": "Option 2", "result": 3}
            ]
        }
    ],
    "results": {
        "1": "Beginner",
        "2": "Intermediate",
        "3": "Advanced"
    }
}
mock_questions_json = json.dumps(mock_questions)

class TestEvaluator(unittest.TestCase):

    def setUp(self):
        pass

    @patch("builtins.open", new_callable=mock_open, read_data='{"questions": [], "results": {}}')
    def test_init(self, mock_file):
        evaluator = Evaluator("user123")
        self.assertEqual(evaluator.user_id, "user123")
        self.assertFalse(evaluator.is_init())
        self.assertFalse(evaluator.is_completed())

    @patch("builtins.open", new_callable=mock_open, read_data=mock_questions_json)
    def test_reset(self, mock_file):
        evaluator = Evaluator("user123")
        evaluator.reset()
        self.assertTrue(evaluator.is_init())
        self.assertFalse(evaluator.is_completed())
        self.assertEqual(evaluator.current_question_id, 1)
        self.assertEqual(evaluator.answers, {})

    @patch("builtins.open", new_callable=mock_open, read_data=mock_questions_json)
    def test_get_next_question(self, mock_file):
        evaluator = Evaluator("user123")
        evaluator.reset()
        question = evaluator.get_next_question()
        self.assertIsInstance(question, TemplateMessage)
        self.assertEqual(question.template.text, "Question 1?")

    @patch("builtins.open", new_callable=mock_open, read_data=mock_questions_json)
    def test_answer_question(self, mock_file):
        evaluator = Evaluator("user123")
        evaluator.reset()
        evaluator.answer_question("Option 1")
        self.assertEqual(evaluator.current_question_id, 2)
        evaluator.answer_question("Option 1")
        self.assertTrue(evaluator.is_completed())
        result = evaluator.get_result()
        self.assertIsInstance(result, TextMessage)
        self.assertIn("Intermediate", result.text)

    @patch("builtins.open", new_callable=mock_open, read_data=mock_questions_json)
    def test_evaluate(self, mock_file):
        evaluator = Evaluator("user123")
        evaluator.reset()
        evaluator.answer_question("Option 2")
        result = evaluator.evaluate()
        self.assertEqual(result, "Beginner")

    @patch("builtins.open", new_callable=mock_open, read_data=mock_questions_json)
    def test_debug(self, mock_file):
        evaluator = Evaluator("user123")
        evaluator.reset()
        evaluator.answer_question("Option 2")
        debug_info = evaluator.debug()
        self.assertIn("User ID: user123", debug_info)
        self.assertIn("評估結果: Beginner", debug_info)

if __name__ == '__main__':
    unittest.main()