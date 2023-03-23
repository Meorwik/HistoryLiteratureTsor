from keyboards.inline.inline_keyboards import callbacks, KeyboardCreator
from data.lesson_material.lesson_materials import questions
from aiogram.dispatcher import FSMContext
from states.states import StateGroup
from loader import dp, bot
from aiogram import types


@dp.message_handler(lambda message: message.text and 'Да, я готов(а) !' in message.text, state=StateGroup.in_quiz)
async def start_quiz(message: types.Message, state: FSMContext):
    keyboard = KeyboardCreator()
    await message.answer(questions["1"]["question"], reply_markup=keyboard.create_keyboard(questions["1"]))
    async with state.proxy() as data:
        data["points"] = 0
        data["question_number"] = 1
        data["keyboard"] = keyboard


@dp.callback_query_handler(state=StateGroup.in_quiz)
async def handle_quiz_callbacks(call: types.CallbackQuery, state: FSMContext):

    if call.data == "CORRECT":
        async with state.proxy() as data:
            data["question_number"] += 1
            data["points"] += 1

    elif call.data == "INCORRECT":
        async with state.proxy() as data:
            data["question_number"] += 1

    async with state.proxy() as data:
        question_number = data["question_number"]
        if question_number <= 10:
            question_data = questions[str(question_number)]
            keyboard = KeyboardCreator().create_keyboard(question_data)
            await call.message.edit_text(questions[str(question_number)]["question"], reply_markup=keyboard)
        else:
            await call.message.delete()
            await bot.send_message(call.from_user.id, text=f"Пройдя викторину, ты набрал: {data['points']}/10 баллов")
            await bot.send_message(call.from_user.id, text="На этом наш урок подошел к концу !")
