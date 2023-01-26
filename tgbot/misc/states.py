from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminMain(StatesGroup):
    main = State()


class AdminEx(StatesGroup):
    get_file = State()


class AdminAdd(StatesGroup):
    get_name = State()
    get_surname = State()
    get_number = State()
    get_job = State()
    get_add = State()
