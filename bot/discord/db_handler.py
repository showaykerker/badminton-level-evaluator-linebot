from typing import Optional
import ezcord

class DBHandler(ezcord.DBHandler):
    def __init__(self, db_path):
        super().__init__(db_path)

    async def setup(self):
        await self.exec("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                username TEXT,
                unfinished_answers_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_interaction_time DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        await self.exec("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                q1 TEXT, q2 TEXT, q3 TEXT, q4 TEXT, q5 TEXT, q6 TEXT, q7 TEXT, q8 TEXT, q9 TEXT, q10 TEXT, q11 TEXT,
                result TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

    async def get_unfinished_answers(self, user_id: str):
        unfinished_answers_id = await self.one("SELECT unfinished_answers_id FROM users WHERE user_id = ?", (user_id,))
        if unfinished_answers_id:
            found = await self.one("SELECT * FROM answers WHERE id = ?", (unfinished_answers_id,))
            return found[2:2+11]
        else:
            return None

    async def update_user(self, user_id: str, username: str):
        # If user already exists, update last_interaction_time, else insert new row
        async with self.start() as cursor:
            if not await self.one("SELECT id FROM users WHERE user_id = ?", (user_id,)):
                await cursor.exec("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
            else:
                await cursor.exec("UPDATE users SET last_interaction_time = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))

    async def add_answer(self, user_id: str, question_id: int, answer: str, result: Optional[str] = None):
        # Check if user has unfinished answers, if not, create a new row in answers table
        async with self.start() as cursor:
            if not await self.one("SELECT unfinished_answers_id FROM users WHERE user_id = ?", (user_id,)):
                async with self.start() as cursor:
                    await cursor.exec("INSERT INTO answers (user_id) VALUES (?)", (user_id,))  # unfinshed_answers_id will be set when insert
                unfinished_answers_id = await self.one("SELECT id FROM answers WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
                async with self.start() as cursor:
                    await cursor.exec("UPDATE users SET unfinished_answers_id = ? WHERE user_id = ?", (unfinished_answers_id, user_id))

            unfinished_answers_id = await self.one("SELECT unfinished_answers_id FROM users WHERE user_id = ?", (user_id,))

        async with self.start() as cursor:
            # Update answers table
            col_name = f"q{question_id}"
            await cursor.exec(f"UPDATE answers SET {col_name} = ? WHERE id = ?", (answer, unfinished_answers_id))

        if result:
            async with self.start() as cursor:
                await cursor.exec("UPDATE users SET unfinished_answers_id = NULL WHERE user_id = ?", (user_id,))
                await cursor.exec("UPDATE answers SET result = ? WHERE id = ?", (result, unfinished_answers_id))