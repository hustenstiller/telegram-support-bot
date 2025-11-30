import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, forward_to_group, forward_to_user
from settings import TELEGRAM_TOKEN, TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID

logging.basicConfig(level=logging.INFO)

def create_application():
    """Create the Telegram bot application (without starting it)."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Chat(
                chat_id=[TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID]
            ),
            forward_to_group,
        )
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & filters.Chat(chat_id=[TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID])
            & filters.REPLY,
            forward_to_user,
        )
    )

    logging.info("Handlers registered.")
    return application

# Do NOT run anything here. Server will start it.
bot_app = create_application()
