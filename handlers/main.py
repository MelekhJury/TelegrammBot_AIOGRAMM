from aiogram.utils import executor
from handlers.create import dp
from data_base import sqlite_db


from handlers import client, admin, other

client.register_hadlers_client(dp)
admin.register_hadlers_admin(dp)
other.register_hadlers_other(dp)

if __name__ == '__main__':
    print("Бот онлайн")
    sqlite_db.sql_start()
    executor.start_polling(dp, skip_updates=True)
