from data.lesson_material.lesson_materials import greece_cities_info, texts
from keyboards.default.default_keyboard import finished_exercise
from keyboards.inline.inline_keyboards import create_city_source_button, create_link_buttons
from states.states import StateGroup
from loader import dp, bot
from aiogram import types


async def messages_filter(message: types.Message):
    return 'Я завершил(а) задание !' in message.text


async def send_city_info(message: types.Message, city_name):
    photo = open(f"data/pictures/{city_name}.jpg", "rb")
    await message.answer_photo(photo=photo, caption=greece_cities_info[city_name], reply_markup=create_city_source_button(city_name))
    photo.close()


@dp.message_handler(messages_filter, state=StateGroup.in_learning)
async def start_quiz(message: types.Message):
    await message.answer(texts['learn_phase_start'])
    await send_city_info(message, "arcadia")
    await send_city_info(message, "stimfal")
    await send_city_info(message, "lerna")
    await send_city_info(message, "nemeya")
    await message.answer(texts['additional_info'], reply_markup=create_link_buttons())
    await message.answer("На этом наш урок закончен, большое спасибо за участие !")

