from aiogram.dispatcher.filters.state import State, StatesGroup


class HaircutState(StatesGroup):
    initialize = State()

    haircut = State()

    afro = State()
    afro_full_head = State()
    afro_undercut = State()

    bred = State()
    bred_full_head = State()
    bred_undercut = State()
    bred_full_head_with_material = State()
    bred_full_head_without_material = State()
    bred_undercut_with_material = State()
    bred_undercut_without_material = State()

    tail = State()