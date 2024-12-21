import os
import json

import discord
import dotenv
from ezcord import Bot, emb

from .messages import more_info as info
from .messages import image_url
from .db_handler import DBHandler
from .utils import get_evaluator, get_statistics_info
from .utils import exec_db_operation, to_safe_string

dotenv.load_dotenv()

bot = Bot()
db_handler = DBHandler("bot/discord/data/user.db")

@bot.slash_command(name="更多資訊", description="檢視專案資訊和分享連結")
async def more_info(ctx):
    pass

@bot.slash_command(name="顯示分級表", description="顯示分級表")
async def level_table(ctx):
    pass

@bot.slash_command(name="統計", description="顯示統計資訊")
async def show_statistics(ctx):
    pass

@bot.slash_command(name="開始測試", description="開始測試")
async def start_test(ctx):
    pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if str(message.author.id) == os.getenv("OWNER_ID"):
        if message.content.startswith("sql "):
            try:
                result = await exec_db_operation(db_handler, message.content[4:])
            except Exception as e:
                result = str(e)
            if result:
                msg = json.dumps(result, indent=4, ensure_ascii=False)
                await message.reply(f"```\n{msg}\n```")
            return
    await db_handler.update_user(message.author.id, message.author.name)
    await db_handler.insert_message(
        message.author.id,
        message.author.name,
        to_safe_string(message.content))

@bot.event
async def on_interaction(interaction):
    if interaction.user.bot:
        return
    await interaction.response.defer()
    await db_handler.update_user(interaction.user.id, interaction.user.name)
    evaluator = None
    if interaction.type != discord.InteractionType.component:
        if interaction.data["name"] == "更多資訊":
            await interaction.edit_original_response(content=info)
        elif interaction.data["name"] == "顯示分級表":
            await interaction.edit_original_response(content=image_url)
        elif interaction.data["name"] == "統計":
            await interaction.edit_original_response(content=await get_statistics_info(interaction, db_handler))
        elif interaction.data["name"] == "開始測試":
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
