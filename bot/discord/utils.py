import discord
from ..core.evaluator import Evaluator
from .db_handler import DBHandler
import os

def to_safe_string(s: str):
    return s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace("`", "'")

def get_evaluator(user_id: str, answers: list[str]) -> Evaluator:
    evaluator = Evaluator(user_id)
    evaluator.reset()
    if answers is not None:
        for answer in answers:
            if answer is None:
                return evaluator
            evaluator.answer_question(answer)
    return evaluator

async def get_messages(db_handler: DBHandler, n=10):
    messages = await db_handler.get_messages(n)
    return messages or []

async def get_statistics_info(interaction: discord.Interaction, db_handler: DBHandler):
    user_count = await db_handler.count_users()
    answer_count = await db_handler.count_answers()
    distribution = await db_handler.get_result_distribution()
    user_id = str(interaction.user.id)
    msg = ""
    if answer_count != 0:
        msg += f"回答數量: {answer_count}\n"
    if distribution:
        msg += f"結果分布: \n"
        for lvl, count in distribution:
            msg += f"\t\t{lvl}: {count}\n"
    if user_id == os.getenv("OWNER_ID"):
        msg += f"使用者數量: {user_count}\n"
        user_name_to_id_dict = {}
        messages = await get_messages(db_handler, 10)
        if messages:
            msg += f"收到的前 {len(messages)} 則訊息:\n"
            for message in messages:
                if message[2] not in user_name_to_id_dict:
                    user_name_to_id_dict[message[2]] = message[1]
                msg += f"- {message[5]} from **{message[2]}** : `{to_safe_string(message[3])}`\n"
            msg += f"使用者名單:\n"
            for user_name, user_id in user_name_to_id_dict.items():
                msg += f"- {user_name} ({user_id})\n"
    return msg