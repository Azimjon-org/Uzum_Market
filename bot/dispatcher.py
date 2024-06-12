from os import getenv

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n
from dotenv import load_dotenv
from redis import Redis

load_dotenv()
i18n = I18n(path="locales")
TOKEN = getenv("TOKEN")

# host=getenv('REDIS_HOST')
# port=getenv('REDIS_PORT')
# redis = Redis(host=host,port=port)
dp = Dispatcher()
