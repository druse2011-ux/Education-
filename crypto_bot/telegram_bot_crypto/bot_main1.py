
# ИМПОРТЫ

# Модуль для работы с операционной системой (например, чтение переменных окружения)
import os

# Модуль для логирования (вывода информации о работе программы)
import logging

# Функция для загрузки переменных окружения из файла .env
from dotenv import load_dotenv

# Импорт классов из библиотеки python-telegram-bot
# Update — объект, содержащий информацию о событии (сообщение, кнопка и т.д.)
from telegram import (
    Update,
    InlineKeyboardButton,   # Кнопка
    InlineKeyboardMarkup,   # Разметка кнопок (клавиатура)
)

# Импорт инструментов для обработки событий (handlers)
from telegram.ext import (
    ApplicationBuilder,     # Создание приложения бота
    ContextTypes,           # Контекст (доп. информация о боте)
    CommandHandler,         # Обработка команд (/start)
    CallbackQueryHandler,   # Обработка нажатий на inline-кнопки
    MessageHandler,         # Обработка обычных сообщений
    filters,                # Фильтры сообщений
)

# Импорт нашей реализации шифра Цезаря
from crypto_bot.src.caesar import CaesarCipher


# =======================
# НАСТРОЙКА ОКРУЖЕНИЯ
# =======================

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен бота из переменной окружения TOKEN
# Это важно — не храним токен прямо в коде (безопасность)
BOT_TOKEN = os.getenv("TOKEN")

# Настраиваем логирование (чтобы видеть ошибки и действия бота в консоли)
logging.basicConfig(level=logging.INFO)


# =======================
# СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЯ
# =======================

# Здесь мы храним состояние каждого пользователя
# Ключ — user_id (уникальный ID пользователя)
# Значение — словарь с параметрами (режим, выбранный шифр и т.д.)
#
# Пример:
# user_state = {
#     123456: {
#         "mode": "encrypt",
#         "cipher": "caesar"
#     }
# }
#
# В реальных проектах это хранят в Redis или базе данных,
# потому что при перезапуске программы словарь очистится
user_state = {}


# =======================
# СОЗДАНИЕ КНОПОК
# =======================

def main_menu():
    """
    Главное меню (inline-кнопки)

    InlineKeyboardButton — отдельная кнопка
    callback_data — данные, которые отправятся боту при нажатии
    """
    keyboard = [
        [InlineKeyboardButton("🔐 Шифровать", callback_data="encrypt")],
        [InlineKeyboardButton("🔓 Дешифровать", callback_data="decrypt")],
    ]

    # InlineKeyboardMarkup — "обёртка" для клавиатуры
    return InlineKeyboardMarkup(keyboard)


def cipher_menu():
    """
    Меню выбора шифра
    """
    keyboard = [
        [InlineKeyboardButton("Caesar", callback_data="caesar")],

        # Здесь можно расширять функциональность:
        # [InlineKeyboardButton("Vigenere", callback_data="vigenere")],
    ]
    return InlineKeyboardMarkup(keyboard)


# =======================
# ХЕНДЛЕРЫ (обработчики)
# =======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start

    Когда пользователь пишет /start,
    Telegram отправляет Update, который попадает сюда
    """

    # update.message — сообщение пользователя
    # reply_text — отправка ответа
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=main_menu()  # прикрепляем кнопки
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработка нажатий на inline-кнопки
    """

    # callback_query — событие нажатия кнопки
    query = update.callback_query

    # Обязательно нужно "ответить" Telegram,
    # иначе кнопка будет висеть в состоянии загрузки
    await query.answer()

    # Получаем ID пользователя
    user_id = query.from_user.id

    # Данные, которые мы указали в callback_data
    data = query.data

    # =======================
    # ВЫБОР РЕЖИМА
    # =======================
    if data in ["encrypt", "decrypt"]:
        # Сохраняем режим пользователя
        user_state[user_id] = {"mode": data}

        # Меняем текст сообщения и показываем меню шифров
        await query.edit_message_text(
            "Выберите шифр:",
            reply_markup=cipher_menu()
        )

    # =======================
    # ВЫБОР ШИФРА
    # =======================
    elif data == "caesar":
        # Добавляем выбранный шифр в состояние
        user_state[user_id]["cipher"] = "caesar"

        # Просим пользователя ввести данные
        await query.edit_message_text(
            "Введите текст и сдвиг через пробел\nПример:\nhello 3"
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработка обычного текста пользователя
    """

    # Получаем ID пользователя
    user_id = update.message.from_user.id

    # Если пользователь не нажал /start — нет состояния
    if user_id not in user_state:
        await update.message.reply_text("Сначала нажмите /start")
        return

    try:
        # Получаем текст сообщения
        text = update.message.text

        # =======================
        # ПАРСИНГ ВВОДА
        # =======================

        # rsplit(" ", 1) — делим строку с конца на 2 части:
        # "hello world 3" → ["hello world", "3"]
        message, shift = text.rsplit(" ", 1)

        # Преобразуем сдвиг в число
        shift = int(shift)

        # Получаем состояние пользователя
        state = user_state[user_id]

        # =======================
        # РАБОТА С ШИФРОМ
        # =======================

        # Создаем объект шифра Цезаря
        cipher = CaesarCipher(shift)

        # В зависимости от режима:
        if state["mode"] == "encrypt":
            result = cipher.encrypt(message)
        else:
            result = cipher.decrypt(message)

        # Отправляем результат пользователю
        await update.message.reply_text(f"Результат:\n{result}")

    # Ошибка, если shift не число или формат неправильный
    except ValueError:
        await update.message.reply_text(
            "Ошибка!\nФормат: текст + число\nПример: hello 3"
        )

    # Любая другая ошибка
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")


# =======================
# ЗАПУСК БОТА
# =======================

def main():
    """
    Точка входа в программу
    """

    # Создаем приложение бота и передаем токен
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # =======================
    # РЕГИСТРАЦИЯ ХЕНДЛЕРОВ
    # =======================

    # Команда /start
    app.add_handler(CommandHandler("start", start))

    # Обработка кнопок
    app.add_handler(CallbackQueryHandler(button_handler))

    # Обработка обычного текста
    # filters.TEXT — только текст
    # ~filters.COMMAND — исключаем команды (/start и т.д.)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Сообщение в консоль
    print("Бот запущен...")

    # Запуск бота (long polling)
    # Бот постоянно опрашивает сервер Telegram:
    # "есть ли новые сообщения?"
    app.run_polling()


# Если файл запущен напрямую (а не импортирован)
if __name__ == "__main__":
    """
    Пользователь пишет /start → бот показывает кнопки
    Пользователь нажимает кнопку → CallbackQueryHandler ловит событие → сохраняем состояние (encrypt/decrypt)
    Пользователь выбирает шифр → сохраняем "caesar"
    Пользователь вводит текст → MessageHandler обрабатывает → парсим текст + число → запускаем шифр → отправляем результат
    """
    main()

