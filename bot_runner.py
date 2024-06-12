import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware
from dotenv import load_dotenv
from bot.handlers import dp
from bot.dispatcher import TOKEN, i18n
from db.config import engine
from db.models import Base
from utils.middlewares import CounterMiddleware

load_dotenv()


def before_start_checker():
    Base.metadata.create_all(engine)


async def all_middlewares():
    dp.update.middleware(CounterMiddleware())
    dp.update.middleware(FSMI18nMiddleware(i18n=i18n))



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(before_start_checker)
    await all_middlewares()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
