from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def start_button():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Сгенерировать ключи 🔑'))
    m.insert(KeyboardButton('Изменить время лицензии ⏳'))
    return m