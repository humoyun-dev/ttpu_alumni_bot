from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class Reg(StatesGroup):
    language = State()
    contact = State()
    first_name = State()
    last_name = State()
    student_id = State()
    is_employed = State()
    work_place = State()
    position = State()
    share_with_employer = State()
    region = State()
    uni_rating = State()
    recommendation = State()
    uni_improvement = State()
    finished = State()
