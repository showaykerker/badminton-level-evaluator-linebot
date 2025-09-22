from typing import Optional, List
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

        await self.exec("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_name TEXT,
                message TEXT,
                read BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

    async def insert_message(self, user_id: str, user_name: str, message: str):
        async with self.start() as cursor:
            await cursor.exec("INSERT INTO messages (user_id, user_name, message) VALUES (?, ?, ?)", (user_id, user_name, message))

    async def get_messages(self, n=10):
        messages = await self.all("SELECT * FROM messages WHERE read = 0 ORDER BY created_at ASC")
        await self.set_message_read([msg[0] for msg in messages])
        return messages

    async def set_message_read(self, message_ids: List[int]):
        async with self.start() as cursor:
            await cursor.exec("UPDATE messages SET read = 1 WHERE id IN ({})".format(", ".join(map(str, message_ids))))

    async def get_unfinished_answers(self, user_id: str):
        unfinished_answers_id = await self.one("SELECT unfinished_answers_id FROM users WHERE user_id = ?", (user_id,))
        if unfinished_answers_id:
            found = await self.one("SELECT * FROM answers WHERE id = ?", (unfinished_answers_id,))
            return found[2:2+11]
        else:
            return None

    async def count_users(self):
        return await self.one("SELECT COUNT(*) FROM users")

    async def count_answers(self):
        return await self.one("SELECT COUNT(*) FROM answers")

    async def get_result_distribution(self):
        def _sort(tup):
            # [('初中階 - 6級', 1), ('新手階 - 1級', 2)]
            data = []
            for item in tup:
                name = item[0]
                data.append((name, item[1]))
            data.sort(
                key=lambda x: int(x[0].split(" - ")[-1].split("級")[0].split("~")[0]),
                reverse=False
            )
            return data
        result = await self.all("SELECT result, COUNT(*) FROM answers GROUP BY result")
        if result:
            result = _sort(result)
        return result

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