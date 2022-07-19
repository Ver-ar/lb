from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import API_KEY

storage = MemoryStorage()
lilabred_bot = Bot(token=API_KEY)
dp = Dispatcher(bot=lilabred_bot, storage=storage)
