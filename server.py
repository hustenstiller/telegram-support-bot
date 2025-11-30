import os
from flask import Flask, request
from telegram import Update
from main import bot_app
import asyncio

TOKEN = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP_NAME = os.environ["HEROKU_APP_NAME"]

WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}"

app = Flask(__name__)

@app.get("/")
def home():
    return "Telegram support bot running."

@app.post(f"/{TOKEN}")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    asyncio.get_event_loop().create_task(bot_app.process_update(update))
    return "OK", 200

async def setup():
    await bot_app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=WEBHOOK_URL,
    )
