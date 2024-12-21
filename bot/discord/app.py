import os
import re
import json

import asyncio
import discord
import dotenv
import ezcord
from ezcord import Bot, emb

from .messages import more_info as info
from .messages import image_url
from .db_handler import DBHandler
from .types_ import User, Answers
from ..core.evaluator import Evaluator
from bot.discord import db_handler

dotenv.load_dotenv()

evaluators = {}

# override the default error embed with a custom one
error_embed = discord.Embed(title="Error", color=discord.Color.orange())
error_embed.set_footer(text="This is a custom footer")

emb.set_embed_templates(error_embed=error_embed)

bot = Bot()
db_handler = DBHandler("user.db")

@bot.slash_command(name="更多資訊")
async def more_info(ctx):
    pass

@bot.slash_command(name="顯示分級表")
async def level_table(ctx):
    pass

@bot.slash_command(name="開始測試")
async def start_test(ctx):
    pass

@bot.event
async def on_interaction(interaction):
    await db_handler.update_user(interaction.user.id, interaction.user.name)
    if interaction.type != discord.InteractionType.component:
        if interaction.data["name"] == "更多資訊":
            await interaction.response.send_message(info)
        elif interaction.data["name"] == "顯示分級表":
            await interaction.response.send_message(image_url)
        elif interaction.data["name"] == "開始測試":
            await interaction.response.defer()
            if interaction.user.id not in evaluators:
                evaluators[interaction.user.id] = Evaluator(interaction.user.name)
                evaluators[interaction.user.id].reset()
            eval_dict = evaluators[interaction.user.id].get_next_question()
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
    if interaction.user.id not in evaluators:
        evaluators[interaction.user.id] = Evaluator(interaction.user.name)
        evaluators[interaction.user.id].reset()
    await interaction.response.defer()
    answer_id = evaluators[interaction.user.id].current_question_id
    answer = interaction.data["custom_id"]
    eval_dict = evaluators[interaction.user.id].answer_question(answer)
    result = None if not eval_dict["is_end"] else eval_dict["level"]
    await db_handler.add_answer(interaction.user.id, answer_id, answer, result=result)
    if eval_dict["is_end"]:
        view = discord.ui.View()
        answer_history_str = evaluators[interaction.user.id].get_answer_history()
        await interaction.edit_original_response(content=answer_history_str, view=view)
        del evaluators[interaction.user.id]
        return
    question = eval_dict["question"]
    options = eval_dict["options"]
    view = discord.ui.View()
    for option in options:
        view.add_item(discord.ui.Button(label=option, custom_id=option))
    await interaction.edit_original_response(content=question, view=view)

bot.run(str(os.getenv("TOKEN")))
