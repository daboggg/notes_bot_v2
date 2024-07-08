from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Button, NumberedPager, Group, StubScroll
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.state_groups import TestDialogSG

texts = ['one', 'two', 'three']
async def save_note_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    scroll: ManagedScroll = dialog_manager.find("text_pages")
    text_number = await scroll.get_page()

    if texts:
        text = texts[text_number]
    else:
        text = "empty"

    return {
        "text_count": len(texts),
        "text_number": text_number + 1,
        "text": text,
    }



async def on_delete_text(
        callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
):
    scroll: ManagedScroll = dialog_manager.find("text_pages")
    text_number = await scroll.get_page()
    del texts[text_number]
    if text_number > 0:
        await scroll.set_page(text_number - 1)



test_dialog = Dialog(
    Window(
        Format("{text}"),
        StubScroll(id="text_pages", pages="text_count"),
        Group(
            NumberedPager(scroll="text_pages", when=F["pages"] > 1),
            width=8,
        ),

        Button(
            Format("🗑️ Удалить файл #{text_number}"),
            id="del",
            on_click=on_delete_text,
            when="text_count",
        ),

        getter=save_note_getter,
        state=TestDialogSG.start
    )
)
