from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


button_load = KeyboardButton("/Создать_директорию")
button_delete = KeyboardButton("/Удалить")


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button_case_admin.row(button_load, button_delete)
