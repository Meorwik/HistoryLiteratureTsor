from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram import types
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Команды: ",
            "/start - Запустить бота",
            "/help - Показать все команды")
    
    await message.answer("\n".join(text))