import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from handlers import start, forward_to_group, forward_to_user
from settings import (
    TELEGRAM_TOKEN,
    TELEGRAM_SUPPORT_CHAT_ID,
    PERSONAL_ACCOUNT_CHAT_ID
)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def create_application():
    """Creates the PTB application and registers all handlers."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # /start command
    application.add_handler(CommandHandler("start", start))

    # Messages from users → forward to support group
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Chat(chat_id=[TELEGRAM_SUPPORT_CHAT_ID, PERSONAL_ACCOUNT_CHAT_ID]),
            forward_to_group,
        )
    )

    # Replies from support or your account → forward back to user
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


# The application instance that server.py will run
bot_app = create_application()
