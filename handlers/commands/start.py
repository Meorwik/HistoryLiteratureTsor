from keyboards.default.default_keyboard import create_agreement_keyboard
from data.lesson_material.lesson_materials import greeting_msg
from aiogram.dispatcher.filters.builtin import CommandStart
from states.states import StateGroup
from aiogram import types
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer(greeting_msg, reply_markup=await create_agreement_keyboard())
    await StateGroup.in_quiz.set()
