import os
import asyncio
from flask import Flask, request
from telegram import Update
from main import bot_app

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

    # PTB v21 async update processing
    asyncio.create_task(bot_app.process_update(update))

    return "OK", 200


async def setup_webhook():
    """Set webhook once on startup"""
    await bot_app.bot.set_webhook(WEBHOOK_URL)


if __name__ == "__main__":
    # Run webhook setup
    asyncio.get_event_loop().run_until_complete(setup_webhook())

    # Start Flask — NOT telegram.run_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
