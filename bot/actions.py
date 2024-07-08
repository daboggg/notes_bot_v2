from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.common import ManagedScroll

from util import number_to_emoji, format_text, translate_content_name


async def get_preview_dict(dialog_manager: DialogManager):

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = get_content(dialog_manager, "photos")

    if photos:
        photo = photos[media_number]
        media = MediaAttachment(
            file_id=MediaId(photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://disk.yandex.ru/i/vO3cLJElrEzT5A",
            # url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637",
            type=ContentType.PHOTO,
        )




    scroll: ManagedScroll = dialog_manager.find("text_pages")
    text_number = await scroll.get_page()
    texts = get_content(dialog_manager,  "texts")
    # texts = dialog_manager.dialog_data.get("texts", [])
    texts = [format_text(text, idx + 1) for idx, text in enumerate(texts)]

    if texts:
        text = texts[text_number]
    else:
        text = "записей нет 🫲 🫱"

    return {
        "note_name": dialog_manager.dialog_data.get("note_name"),
        "category_name": dialog_manager.dialog_data.get("category_name"),
        "text_count": len(texts),
        "text_number": text_number + 1,
        "text": text,
        "media_count": len(photos),
        "media_number": media_number + 1,
        "media": media,
    }


# без аргумента возвращается весь контент, а с аргументом - список
def get_content(dialog_manager: DialogManager, type_data: str = None) -> dict or list:
    if type_data is None:
        return dialog_manager.dialog_data.get("content", {})
    else:
        return dialog_manager.dialog_data.get("content").get(type_data, [])


def counting_elements(dialog_manager) -> str:
    """
        Подсчитывает введенные записи и файлы
    """
    if get_content(dialog_manager):
        result_str = "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
    else:
        result_str = ""
    for key, value in get_content(dialog_manager).items():
        result_str += f"{translate_content_name(key)}: {number_to_emoji(len(value))}\n"
    return result_str
