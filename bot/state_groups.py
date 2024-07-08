from aiogram.fsm.state import StatesGroup, State


class MainDialogSG(StatesGroup):
    get_content = State()
    get_note_name = State()
    get_category_name = State()
    save_note = State()


class TestDialogSG(StatesGroup):
    start = State()