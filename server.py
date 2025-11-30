import os
import asyncio
from flask import Flask, request
from telegram import Update
from main import bot_app

TOKEN = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP_NAME = os.environ["HEROKU_APP_NAME"]

WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/webhook/{TOKEN}"

app = Flask(__name__)

@app.get("/")
def home():
    return "Bot is running."

@app.post(f"/webhook/{TOKEN}")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    asyncio.get_event_loop().create_task(bot_app.process_update(update))
    return "OK", 200

async def setup_webhook():
    await bot_app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(setup_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
