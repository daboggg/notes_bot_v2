from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from settings import settings

bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
