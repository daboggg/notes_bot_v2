from pprint import pprint

from aiogram import F
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Bold, Italic
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, StubScroll, Group, NumberedPager, Row, SwitchTo, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.actions import counting_elements, get_preview_dict, get_content
from bot.state_groups import MainDialogSG


##### getters ###############################################################


async def get_content_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        "content": counting_elements(dialog_manager)
    }


async def get_note_name_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        "content": counting_elements(dialog_manager)
    }


async def get_category_name_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        "content": counting_elements(dialog_manager),
        "note_name": dialog_manager.dialog_data.get("note_name"),
    }


async def save_note_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return await get_preview_dict(dialog_manager)


###### handlers ##############################################################
async def message_handler(message: Message, message_input, dialog_manager: DialogManager):
    content = dialog_manager.dialog_data.setdefault("content", {})
    if message.text:
        content.setdefault("texts", [])
        content.get("texts").append(message.text)
        # dialog_manager.dialog_data.setdefault("texts", [])
        # dialog_manager.dialog_data.get("texts").append(message.text)
    elif message.photo:
        content.setdefault("photos", [])
        content.get("photos").append(message.photo[-1].file_id)

    pprint(dialog_manager.dialog_data)


async def note_name_handler(message: Message, widget, dialog_manager: DialogManager, data: str, /):
    dialog_manager.dialog_data["note_name"] = data
    await dialog_manager.switch_to(MainDialogSG.get_category_name)


async def category_name_handler(message: Message, widget, dialog_manager: DialogManager, data: str, /):
    dialog_manager.dialog_data["category_name"] = data
    await dialog_manager.switch_to(MainDialogSG.save_note)


# async def on_text_selected(callback: CallbackQuery, widget: Any,
#                            dialog_manager: DialogManager, item_id: str):
#     del dialog_manager.dialog_data.get("texts")[int(item_id)]
#
#
async def on_next_button(
        callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data.get("note_name") and dialog_manager.dialog_data.get("note_name"):
        await dialog_manager.switch_to(MainDialogSG.save_note)
    else:
        await dialog_manager.switch_to(MainDialogSG.get_note_name)


async def on_delete_file(
        callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
):
    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = get_content(dialog_manager, "photos")
    del photos[media_number]
    if media_number > 0:
        await scroll.set_page(media_number - 1)


async def on_delete_text(
        callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
):
    scroll: ManagedScroll = dialog_manager.find("text_pages")
    text_number = await scroll.get_page()
    texts = get_content(dialog_manager, "texts")
    del texts[text_number]
    if text_number > 0:
        await scroll.set_page(text_number - 1)


async def on_save_button(
        callback: CallbackQuery, widget: Button, dialog_manager: DialogManager,
):
    print("Saved")
    await callback.answer("Сохранено")
    await dialog_manager.start(state=MainDialogSG.get_content, mode=StartMode.RESET_STACK)


main_dialog = Dialog(
    Window(
        Const(Bold('Введите текст записи или добавьте фото, видео, файл или голосовое сообщение').as_html()),
        Format("{content}"),
        MessageInput(
            message_handler,
            content_types=[
                ContentType.TEXT,
                ContentType.PHOTO,
                ContentType.VIDEO,
                ContentType.VIDEO_NOTE,
                ContentType.DOCUMENT,
                ContentType.AUDIO,
                ContentType.VOICE,
            ]
        ),
        Button(Const("Далее"), when=F["content"], on_click=on_next_button, id="next_button"),
        getter=get_content_getter,
        state=MainDialogSG.get_content

    ),
    Window(
        Const(Bold("Введите название записки").as_html()),
        Format("{content}"),
        TextInput(
            id="note_name",
            on_success=note_name_handler
        ),
        Back(Const("Назад")),
        getter=get_note_name_getter,
        state=MainDialogSG.get_note_name
    ),
    Window(
        Const(Bold("Введите название раздела").as_html()),
        Format("{content}"),
        Format(Italic("записка: ").as_html() + "{note_name}"),
        TextInput(
            id="category_name",
            on_success=category_name_handler
        ),
        Back(Const("Назад")),
        getter=get_category_name_getter,
        state=MainDialogSG.get_category_name
    ),
    Window(
        DynamicMedia(selector="media"),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(id="media", scroll="pages", when=F["pages"] > 1),
            width=8,
        ),

        Button(
            Format("🗑️ Удалить файл #{media_number}"),
            id="del",
            on_click=on_delete_file,
            when="media_count",
        ),

        Format("{text}"),
        StubScroll(id="text_pages", pages="text_count"),
        Group(
            NumberedPager(id="text", scroll="text_pages", when=F["pages"] > 1),
            width=8,
        ),
        Format(Italic("записка: ").as_html() + "{note_name}"),
        Format(Italic("раздел: ").as_html() + "{category_name}"),
        Button(
            Format("🗑️ Удалить текст #{text_number}"),
            id="del_text",
            on_click=on_delete_text,
            when="text_count",
        ),

        Row(
            SwitchTo(Const("Добавить"), state=MainDialogSG.get_content, id="add_note"),
            Start(Const("Удалить"), state=MainDialogSG.get_content, mode=StartMode.RESET_STACK, id="reset_stack")
        ),
        Row(
            Back(Const("Назад")),
            Button(Const("Сохранить"), on_click=on_save_button, id="save_notes"),
        ),
        getter=save_note_getter,
        state=MainDialogSG.save_note
    )
)
