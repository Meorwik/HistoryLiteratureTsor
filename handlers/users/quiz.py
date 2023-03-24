from data.lesson_material.lesson_materials import texts, quiz_questions
from keyboards.default.default_keyboard import finished_exercise
from keyboards.inline.inline_keyboards import KeyboardCreator
from aiogram.dispatcher import FSMContext
from states.states import StateGroup
from loader import dp, bot
from aiogram import types


async def send_question_with_photo(message: types.Message, num: int, question_number):
    await message.delete()
    photo = open(f"data/pictures/{num}.jpg", "rb")
    keyboard = KeyboardCreator().create_keyboard(quiz_questions[question_number])
    await message.answer_photo(photo, quiz_questions[question_number]["question"], reply_markup=keyboard)
    photo.close()


async def rate_student(message: types.Message, points: int):
    await message.answer(text=f"Пройдя викторину, ты набрал: {points}/10 баллов")

    if points <= 6:
        await message.answer(texts["bad_rating"])
    elif points > 6:
        await message.answer(texts["good_rating"])


async def message_filter(message: types.Message):
    return 'Да, я готов(а) !' in message.text


@dp.message_handler(message_filter, state=StateGroup.in_quiz)
async def start_quiz(message: types.Message, state: FSMContext):
    photo = open("data/pictures/quize_start.jpg","rb")
    await message.answer_photo(photo=photo)
    await message.answer\
        (
            text=quiz_questions["1"]["question"],
            reply_markup=KeyboardCreator().create_keyboard(quiz_questions["1"])
        )
    photo.close()

    async with state.proxy() as data:
        data["points"] = 0
        data["question_number"] = 1


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
        question_number = str(data["question_number"])
        if int(question_number) <= 10:

            if question_number == "2":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
                await send_question_with_photo(call.message, 1, question_number)

            elif question_number == "4":
                await send_question_with_photo(call.message, 2, question_number)

            elif question_number == "7":
                await send_question_with_photo(call.message, 3, question_number)

            else:
                await call.message.delete()
                keyboard = KeyboardCreator().create_keyboard(quiz_questions[question_number])
                await call.message.answer(quiz_questions[question_number]["question"], reply_markup=keyboard)

        else:
            await call.message.delete()
            await rate_student(call.message, data["points"])
            second_part_photo = open("data/pictures/second_part.jpg", "rb")
            await call.message.answer_photo(photo=second_part_photo, caption=texts["second_part_intro"], reply_markup=await finished_exercise())
            await StateGroup.in_learning.set()
            second_part_photo.close()
