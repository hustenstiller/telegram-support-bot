import os
from flask import Flask, request
from main import bot  # import your existing bot instance

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
APP_NAME = os.environ.get("HEROKU_APP_NAME")

WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://{APP_NAME}.herokuapp.com{WEBHOOK_PATH}"

@app.route("/", methods=["GET"])
def index():
    return "Support bot running!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([bot._parse_update(update)])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
