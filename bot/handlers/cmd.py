from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram_dialog import DialogManager, StartMode

from bot.state_groups import MainDialogSG, TestDialogSG

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainDialogSG.get_content, mode=StartMode.RESET_STACK)


@cmd_router.message(Command(commands="test"))
async def test(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(TestDialogSG.start, mode=StartMode.RESET_STACK)

