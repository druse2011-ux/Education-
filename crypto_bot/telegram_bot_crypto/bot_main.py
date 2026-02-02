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

# from .src.caesar import encrypt_caesar_code, decrypt_caesar_code

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


def encrypt_caesar_code(text: str, shift: int) -> str:
    english_alphabet = "abcdefghijklmnopqrstvupwxyz"
    russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    list_elements_text = []
    for element in text:
        if element.lower() in english_alphabet or element.isalpha() is False:
            if element.islower():
                new_code = (ord(element) - ord("a") + shift) % 26 + ord("a")
                list_elements_text.append(chr(new_code))
            elif element.isupper():
                new_code = (ord(element) - ord("A") + shift) % 26 + ord("A")
                list_elements_text.append(chr(new_code))
            else:
                list_elements_text.append(element)
        elif element.lower() in russia_alphabet:
            if element.islower():
                new_code = (ord(element) - ord("а") + shift) % 33 + ord("а")
                list_elements_text.append(chr(new_code))
            else:
                new_code = (ord(element) - ord("А") + shift) % 33 + ord("А")
                list_elements_text.append(chr(new_code))
        else:
            break
    if len(list_elements_text) == len(text):
        return "".join(list_elements_text)
    else:
        return (
            "Ошибка ввода. Бот принимает текст только на английском или русском языке!"
        )


def decrypt_caesar_code(text: str, shift: int) -> str:
    return encrypt_caesar_code(text, -shift)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    shifr_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), shifr)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(shifr_handler)
    application.add_handler(echo_handler)
    application.run_polling()
