import sqlite3

from .models import DiscordUser

def discord_user_to_dict(discord_user: DiscordUser):
    return {
        "discord_id": discord_user.discord_id,
        "name": discord_user.name,
        "next_question_id": discord_user.questionaire.current_question_id
    }

def discord_user_from_selected(discord_user_dict: list):
    return DiscordUser(
        discord_id=discord_user_dict[1],
        name=discord_user_dict[2],
        questionaire=discord_user_dict[3]
    )

class SQLiteAdapter:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS discord_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id TEXT,
                name TEXT,
                next_question_id INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def add_user(self, discord_user: DiscordUser):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO discord_users (discord_id, name, next_question_id)
            VALUES (?, ?, ?)
        ''', (discord_user.discord_id, discord_user.name, discord_user.questionaire.current_question_id))
        conn.commit()
        conn.close()