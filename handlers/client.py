from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create import bot, dp
from data_base import sqlite_db
from aiogram.dispatcher.filters import Text
from keyboards import klient_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID_user = None
adress  = None

class FSMUser(StatesGroup):
    home = State()

#------------------------Приветствие и направление сообщения как общаться с ботом--------------------------------
async def command_start(message: types.message):
    try:
        await bot.send_message(message.from_user.id, "Добро пожаловать в бота для загрузки ДЗ"
                                                     " группы №162", reply_markup=klient_kb)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС:\n"
                            "https://t.me/ITOVERONE_162bot")
#-----------------------------------------Справка о работе бота--------------------------------------------------
async def command_help(message: types.message):
    await bot.send_message(message.from_user.id, "Алгоритм загрузки ДЗ:\n"
                                                 "1. Нажмите на кнопку директория\n"
                                                 "2. Выберите свою ФИО\n"
                                                 "3. Нажмите на кнопку загрузить\n"
                                                 "4. Отправьте картинку\n"
                                                 "Примечание:\n"
                                                 "В случае отправки картинки с ПК "
                                                 "необходимо обязательно поставить галочку сжать изображение\n"
                                                 "\n"
                                                 "Алгоритм просмотра ДЗ:\n"
                                                 "1. Нажмите на кнопку Группа\n"
                                                 "2. Выберите свою ФИО",
                                                 reply_markup=klient_kb)
    await message.delete()

# -------------------------------------------Кнопка ОТМЕНЫ-------------------------------------------------------
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Загрузка отменена")
#------------Выбор директории для загрузки ДЗ(Получение id-шника по которому будем загружать ДЗ)-----------------
async def callback_run(callback_query: types.CallbackQuery):
    global adress
    adress = callback_query.data.replace("add ", "")
    await callback_query.answer(text=f"Директория выбрана",
                                show_alert=True)

async def choise_directory(message: types.Message):
    await message.reply("Выберите свою директорию:")
    read = await sqlite_db.sql_read()
    for ret in read:
        await bot.send_message(message.from_user.id, text=f"{ret[1]}",
                               reply_markup=InlineKeyboardMarkup().
                               add(InlineKeyboardButton(f"Выбрать",
                                                        callback_data=f"add {ret[0]}")))
# -------------------------------------------Загрузка ДЗ---------------------------------------------------------
# ------------------------------------Инициализация машины состояний---------------------------------------------
async def home_task_1(message: types.Message):
    if adress == None:
        await bot.send_message(message.from_user.id, "Не выбрана директория для загрузки")
    else:
        await FSMUser.home.set()
        await message.reply("Добавьте фото с домашним заданием")

async def home_task_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["home"] = message.photo[0].file_id
        data["id_student"] = adress
    await sqlite_db.sql_add_home_command(state)
    await message.reply("Готово")
    await state.finish()

# ------------------------------------Комманда для просмотра ДЗ--------------------------------------------------
async def command_group(message: types.Message):
    read = await sqlite_db.sql_read()
    global ID_user
    ID_user = message.from_user.id
    for ret in read:
        await bot.send_message(message.from_user.id, text=f"{ret[1]}",
                               reply_markup=InlineKeyboardMarkup().
                               add(InlineKeyboardButton(f"Просмотр ДЗ",
                                                        callback_data=f"home check{ret[0]}")))

async def callback_check_home(callback_home: types.CallbackQuery):
    read = await sqlite_db.sql_read_home(callback_home.data.replace('home check', ''))
    await bot.send_message(ID_user, "Домашнее задание выбранного студента")
    for pictures in read:
        await bot.send_photo(ID_user, pictures[0])
    await callback_home.answer()


def register_hadlers_client(dp:Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])

    dp.register_message_handler(command_help,  commands=["Помощь"])

    #--------хендлер просмотра ДЗ-----------
    dp.register_message_handler(command_group, commands=["Группа"])
    dp.register_callback_query_handler(callback_check_home, lambda x: x.data and x.data.startswith("home check"))

    #--------Хендлер ОТМЕНЫ---------
    dp.register_message_handler(cancel_handler, state="*", commands="Отмена")
    dp.register_message_handler(cancel_handler, Text(equals="Отмена", ignore_case=True), state="*")

    #--------Хендлеры загрузки ДЗ--------
    dp.register_message_handler(choise_directory, commands=["Директория"])
    dp.register_callback_query_handler(callback_run, lambda x: x.data and x.data.startswith("add "))
    dp.register_message_handler(home_task_1,      commands=["Загрузить"])
    dp.register_message_handler(home_task_2,      content_types=["photo"], state=FSMUser.home)
