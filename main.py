import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters
)
from handlers import start, forward_to_group, forward_to_user
from settings import TELEGRAM_TOKEN, TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # messages from users → support group
    app.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Chat([TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID]),
            forward_to_group,
        )
    )

    # replies from support → user
    app.add_handler(
        MessageHandler(
            filters.TEXT
            & filters.Chat([TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID])
            & filters.REPLY,
            forward_to_user,
        )
    )

    logging.info("Handlers registered.")
    return app

bot_app = create_app()
