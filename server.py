import os
import asyncio
from flask import Flask, request
from telegram import Update
from main import bot_app

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP_NAME = os.environ["HEROKU_APP_NAME"]

WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/webhook/{TOKEN}"


@app.get("/")
def home():
    return "Bot running"


@app.post(f"/webhook/{TOKEN}")
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)

    # schedule async PTB update handling
    asyncio.run(bot_app.process_update(update))
    return "OK", 200


@app.before_first_request
def register_webhook():
    asyncio.run(bot_app.bot.set_webhook(WEBHOOK_URL))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
