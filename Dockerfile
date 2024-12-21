FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

VOLUME [ "/app/bot/discord/data" ]
COPY . .

CMD ["python", "-m", "bot.discord.app"]
