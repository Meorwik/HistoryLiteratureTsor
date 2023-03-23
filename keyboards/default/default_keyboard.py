from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def create_agreement_keyboard():
    agree_button = KeyboardButton("Да, я готов(а) !")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(agree_button)
    return keyboard

