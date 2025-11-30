import os
from main import bot_app

TOKEN = os.environ["TELEGRAM_TOKEN"]
HEROKU_APP_NAME = os.environ["HEROKU_APP_NAME"]

WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/webhook/{TOKEN}"

if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=WEBHOOK_URL,
        secret_token=TOKEN,
        endpoint=f"/webhook/{TOKEN}",
    )
