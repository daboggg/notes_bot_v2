from aiogram.enums import ContentType
from aiogram.utils.formatting import Italic


def number_to_emoji(num: int) -> str:
    result: str = ""
    for n in str(num):
        match n:
            case "0":
                result += "0️⃣"
            case "1":
                result += "1️⃣"
            case "2":
                result += "2️⃣"
            case "3":
                result += "3️⃣"
            case "4":
                result += "4️⃣"
            case "5":
                result += "5️⃣"
            case "6":
                result += "6️⃣"
            case "7":
                result += "7️⃣"
            case "8":
                result += "8️⃣"
            case "9":
                result += "9️⃣"

    return result


def format_text(text: str, position: int) -> str:
    return f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n" \
           f"запись {number_to_emoji(position)}\n" \
           f"{text}\n" \
           f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"

def translate_content_name(text: str) -> str:
    content_name = {
        "texts": Italic("записи").as_html(),
        "photos": Italic("фото").as_html(),
    }
    return content_name.get(text, text)


def get_type_content(content: str) -> ContentType:
    if content == "texts":
        return ContentType.TEXT
    elif content == "photos":
        return ContentType.PHOTO
    else:
        return ContentType.TEXT