import os

import discord
import dotenv
from ezcord import Bot, emb

from .messages import more_info as info
from .messages import image_url
from .db_handler import DBHandler
from ..core.evaluator import Evaluator

dotenv.load_dotenv()

# override the default error embed with a custom one
error_embed = discord.Embed(title="Error", color=discord.Color.orange())
error_embed.set_footer(text="This is a custom footer")

emb.set_embed_templates(error_embed=error_embed)

bot = Bot()
db_handler = DBHandler("bot/discord/data/user.db")

@bot.slash_command(name="更多資訊", description="檢視專案資訊")
async def more_info(ctx):
    pass

@bot.slash_command(name="顯示分級表", description="顯示分級表")
async def level_table(ctx):
    pass

@bot.slash_command(name="開始測試", description="開始測試")
async def start_test(ctx):
    pass

@bot.slash_command(name="分享連結", description="顯示分享連結")
async def share_link(ctx):
    pass

@bot.slash_command(name="統計", description="顯示統計資訊")
async def statistic(ctx):
    pass

def get_evaluator(user_id: str, answers: list[str]) -> Evaluator:
    evaluator = Evaluator(user_id)
    evaluator.reset()
    if answers is not None:
        for answer in answers:
            if answer is None:
                return evaluator
            evaluator.answer_question(answer)
    return evaluator

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await db_handler.update_user(message.author.id, message.author.name)
    await db_handler.insert_message(message.author.id, message.author.name, message.content)

async def get_messages(n=10):
    messages = await db_handler.get_messages(n)
    return messages or []

def to_safe_string(s: str):
    return s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace("`", "'")

async def statistics(interaction):
    user_count = await db_handler.count_users()
    answer_count = await db_handler.count_answers()
    distribution = await db_handler.get_result_distribution()
    user_id = str(interaction.user.id)
    msg = ""
    if user_id == os.getenv("OWNER_ID"):
        msg += f"使用者數量: {user_count}\n"
    if answer_count != 0:
        msg += f"回答數量: {answer_count}\n"
    if distribution:
        msg += f"結果分布: \n"
        for lvl, count in distribution:
            msg += f"\t\t{lvl}: {count}\n"
    if user_id == os.getenv("OWNER_ID"):
        user_name_to_id_dict = {}
        messages = await get_messages(10)
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


@bot.event
async def on_interaction(interaction):
    if interaction.user.bot:
        return
    await db_handler.update_user(interaction.user.id, interaction.user.name)
    evaluator = None
    if interaction.type != discord.InteractionType.component:
        if interaction.data["name"] == "分享連結":
            msg = f"羽球等級評估機器人 on Discord\nhttps://discord.com/oauth2/authorize?client_id=1318915531994042448"
            await interaction.response.send_message(msg)
        elif interaction.data["name"] == "統計":
            msg = await statistics(interaction)
            await interaction.response.send_message(msg)
        elif interaction.data["name"] == "更多資訊":
            await interaction.response.send_message(info)
        elif interaction.data["name"] == "顯示分級表":
            await interaction.response.send_message(image_url)
        elif interaction.data["name"] == "開始測試":
            await interaction.response.defer()
            found_in_db = await db_handler.get_unfinished_answers(interaction.user.id)
            evaluator = get_evaluator(interaction.user.id, found_in_db)
            eval_dict = evaluator.get_next_question()
            if eval_dict["is_end"]:
                await interaction.edit_original_response(content=eval_dict["level"])
                return
            question = eval_dict["question"]
            options = eval_dict["options"]
            view = discord.ui.View()
            for option in options:
                view.add_item(discord.ui.Button(label=option, custom_id=option))
            await interaction.edit_original_response(content=question, view=view)
        return
    if evaluator is None:
        found_in_db = await db_handler.get_unfinished_answers(interaction.user.id)
        evaluator = get_evaluator(interaction.user.id, found_in_db)
    await interaction.response.defer()
    answer_id = evaluator.current_question_id
    answer = interaction.data["custom_id"]
    eval_dict = evaluator.answer_question(answer)
    result = None if not eval_dict["is_end"] else eval_dict["level"]
    await db_handler.add_answer(interaction.user.id, answer_id, answer, result=result)
    if eval_dict["is_end"]:
        view = discord.ui.View()
        answer_history_str = evaluator.get_answer_history()
        await interaction.edit_original_response(content=answer_history_str, view=view)
        return
    question = eval_dict["question"]
    options = eval_dict["options"]
    view = discord.ui.View()
    for option in options:
        view.add_item(discord.ui.Button(label=option, custom_id=option))
    await interaction.edit_original_response(content=question, view=view)

bot.run(str(os.getenv("TOKEN")))
