from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = '5140498173:AAEdS0lAfsiPGLaxuVEK7lslRqoo_nUYGDA'

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

