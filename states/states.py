from aiogram.dispatcher.filters.state import State, StatesGroup


class StateGroup(StatesGroup):
    in_quiz = State()
    in_learning = State()

