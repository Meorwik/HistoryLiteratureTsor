from data.lesson_material.lesson_materials import questions, greeting_msg
from keyboards.inline.inline_keyboards import KeyboardCreator
from aiogram.dispatcher.filters.builtin import CommandStart
from handlers.users.quiz import start_quiz
from keyboards.default.default_keyboard import create_agreement_keyboard
from states.states import StateGroup
from aiogram import types
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer(greeting_msg, reply_markup=await create_agreement_keyboard())
    await StateGroup.in_quiz.set()
