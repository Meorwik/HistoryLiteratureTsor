from data.lesson_material.lesson_materials import quiz_introduction, quiz_questions
from keyboards.default.default_keyboard import finished_exercise
from keyboards.inline.inline_keyboards import KeyboardCreator
from aiogram.dispatcher import FSMContext
from states.states import StateGroup
from loader import dp, bot
from aiogram import types


@dp.message_handler(lambda message: message.text and 'Да, я готов(а) !' in message.text, state=StateGroup.in_quiz)
async def start_quiz(message: types.Message, state: FSMContext):

    keyboard = KeyboardCreator()
    await message.answer(quiz_introduction)
    await message.answer(quiz_questions["1"]["question"], reply_markup=keyboard.create_keyboard(quiz_questions["1"]))

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
            question_data = quiz_questions[str(question_number)]
            keyboard = KeyboardCreator().create_keyboard(question_data)
            if question_number == 2:
                await bot.delete_message(message_id=call.message.message_id-1, chat_id=call.from_user.id)
                await call.message.delete()
                photo = open("data/pictures/1.jpg", "rb")
                await bot.send_photo(photo=photo, caption=quiz_questions[str(question_number)]["question"], reply_markup=keyboard, chat_id=call.from_user.id)
                photo.close()
            elif question_number == 4:
                await call.message.delete()
                photo = open("data/pictures/2.jpg", "rb")
                await bot.send_photo(photo=photo, caption=quiz_questions[str(question_number)]["question"], reply_markup=keyboard, chat_id=call.from_user.id)
                photo.close()
            elif question_number == 7:
                await call.message.delete()
                photo = open("data/pictures/3.jpg", "rb")
                await bot.send_photo(photo=photo, caption=quiz_questions[str(question_number)]["question"], reply_markup=keyboard, chat_id=call.from_user.id)
                photo.close()
            else:
                await call.message.delete()
                await bot.send_message(chat_id=call.from_user.id, text=quiz_questions[str(question_number)]["question"], reply_markup=keyboard)

        else:
            await call.message.delete()
            await bot.send_message(call.from_user.id, text=f"Пройдя викторину, ты набрал: {data['points']}/10 баллов")
            if data['points'] <= 6:
                await bot.send_message(call.from_user.id, text="Неплохо, но ты можешь лучше !")
            elif data["points"] > 6:
                await bot.send_message(call.from_user.id, text="Это очень хороший результат !\nТы молодец!")

            await bot.send_message(call.from_user.id, text="А сейчас мы переходим к следующей части урока\nhttps://learningapps.org/20806237\nПройди задание по этой ссылке и нажми на кнопку по завершению.", reply_markup=await finished_exercise())
            await StateGroup.in_learning.set()
