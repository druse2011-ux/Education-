from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from crypto_bot.src.caesar import encrypt_caesar_code, decrypt_caesar_code

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я бот-шифровальщик, пожалуйста напишите текст мне",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def shifr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text0 = encrypt_caesar_code(update.message.text[:-2], int(update.message.text[-1]))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text0)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    shifr_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), shifr)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(shifr_handler)
    application.add_handler(echo_handler)
    application.run_polling()
