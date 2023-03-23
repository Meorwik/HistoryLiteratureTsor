from data.config.config import ADMINS
from aiogram import Dispatcher


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        await dp.bot.send_message(admin, "Бот запущен!")
