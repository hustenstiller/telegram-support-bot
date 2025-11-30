import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from handlers import start, forward_to_group, forward_to_user
from settings import TELEGRAM_TOKEN, TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID

logging.basicConfig(level=logging.INFO)

# Telegram application
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Flask web server
app = Flask(__name__)

# Register handlers
application.add_handler(start)
application.add_handler(forward_to_group)
application.add_handler(forward_to_user)

@app.post(f"/webhook")
async def webhook():
    """Receives updates from Telegram."""
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "OK", 200

@app.get("/")
def home():
    return "Bot is running!", 200


async def set_webhook():
    url = os.getenv("APP_URL")   # example: https://yourappname.herokuapp.com
    webhook_url = f"{url}/webhook"

    logging.info(f"Setting webhook to: {webhook_url}")
    await application.bot.set_webhook(webhook_url)


if __name__ == "__main__":
    import asyncio

    # Set webhook on startup
    asyncio.run(set_webhook())

    # Start Flask server for Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
