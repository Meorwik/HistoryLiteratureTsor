from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Команда start для начала урока"),
            types.BotCommand("help", "Команда help для помощи с ботом"),
        ]
    )
