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


def create_inline_source_button(name):
    button = InlineKeyboardButton("Больше информации -->", url=city_sources[name])
    return InlineKeyboardMarkup(row_width=1).add(button)
