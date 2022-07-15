from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# Кнопки с общей информацией
button_start = KeyboardButton("/start")
button_help = KeyboardButton("/Помощь")
button_group = KeyboardButton("/Группа")
button_load = KeyboardButton("/Загрузить")
button_student = KeyboardButton("/Директория")
button_cancel = KeyboardButton("/Отмена")

klient_kb = ReplyKeyboardMarkup(resize_keyboard=True)

klient_kb.row(button_start, button_help, button_group)
klient_kb.add(button_load, button_student,button_cancel)

