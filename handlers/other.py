from aiogram import types, Dispatcher
from handlers.create import dp
import json, string


async def uncesored(message: types.Message):
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split("  ")}\
            .intersection(set(json.load(open("D:/HomeWorkTeleBot/handlers/cenz.json")))) != set():
        await message.reply("Не материтесь")
        await message.delete()

def register_hadlers_other(dp : Dispatcher):
    dp.register_message_handler(uncesored)
