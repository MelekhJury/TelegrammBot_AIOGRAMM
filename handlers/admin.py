from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from handlers.create import dp, bot
from data_base import sqlite_db
from aiogram.dispatcher.filters import Text
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

class FSMAdmin(StatesGroup):
    student = State()

async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Модерирование группы",
          reply_markup=admin_kb.button_case_admin)
    await message.delete()

async def student_task(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.student.set()
        await message.reply("Введите ФИО ученика")

# Загрузка ученика

async def load_student(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["student"] = message.text
        await sqlite_db.sql_add_stud_command(state)
        await message.reply("Готово")
        await state.finish()

async def del_callback_run(callback: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback.data.replace('del ', ''))
    await callback.answer(text=f"Студент удален", show_alert=True)

async def delete_student(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read()
        for ret in read:
            await bot.send_message(message.from_user.id, text=f"{ret[1]}",
                                   reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton(f"Удалить",
                                                            callback_data=f"del {ret[0]}")))

def register_hadlers_admin(dp:Dispatcher):
    dp.register_message_handler(student_task, commands=["Создать_директорию"])
    dp.register_message_handler(delete_student, commands=["Удалить"])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith("del "))
    dp.register_message_handler(load_student, state=FSMAdmin.student)
    dp.register_message_handler(make_changes_command, commands=["moder"], is_chat_admin=True)
