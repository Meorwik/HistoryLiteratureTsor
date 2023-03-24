from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.lesson_material.lesson_materials import city_sources
from random import shuffle
from aiogram import types

CORRECT_ANSWER_CALLBACK = "CORRECT"
INCORRECT_ANSWER_CALLBACK = "INCORRECT"


class KeyboardCreator:
    def __init__(self):
        self.__keyboard = InlineKeyboardMarkup(row_width=1)
        self.__question = None
        self.__all_buttons = []

    def __create_correct_answer_button(self):
        correct_answer_button = InlineKeyboardButton\
            (
                self.__question["correct_answer"],
                callback_data=CORRECT_ANSWER_CALLBACK
            )
        return [correct_answer_button]

    def __create_incorrect_answer_buttons(self):
        incorrect_buttons = \
            [
                InlineKeyboardButton(text, callback_data=INCORRECT_ANSWER_CALLBACK)
                for text in
                self.__question["incorrect_answers"].values()
            ]
        return incorrect_buttons

    def create_keyboard(self, question: dict):
        self.__keyboard.clean()
        self.__question = question
        self.__all_buttons += self.__create_correct_answer_button()
        self.__all_buttons += self.__create_incorrect_answer_buttons()
        shuffle(self.__all_buttons)
        return self.__keyboard.add(*self.__all_buttons)


def create_city_source_button(name):
    button = InlineKeyboardButton("Больше информации -->", url=city_sources[name])
    return InlineKeyboardMarkup(row_width=1).add(button)


def create_link_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    cartoon_1_button = InlineKeyboardButton("Мультфильм", url="https://youtu.be/QsK3fxALfU8")
    cartoon_2_button = InlineKeyboardButton("11 подвиг Геракла", url="https://www.youtube.com/watch?v=Yz93dQp3k3Y&feature=youtu.be")
    mify_button = InlineKeyboardButton("Мифы Древней Греции", url="https://teremok.in/Mifologija/Mifi_gretsii.htm")
    keyboard.add(cartoon_1_button, cartoon_2_button, mify_button)
    return keyboard



