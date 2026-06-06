from aiogram.fsm.state import State, StatesGroup


class StudyStates(StatesGroup):
    choosing_count = State()
    in_round = State()
