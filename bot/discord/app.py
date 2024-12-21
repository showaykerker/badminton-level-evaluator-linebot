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
async def on_interaction(interaction):
    await db_handler.update_user(interaction.user.id, interaction.user.name)
    evaluator = None
    if interaction.type != discord.InteractionType.component:
        if interaction.data["name"] == "更多資訊":
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
