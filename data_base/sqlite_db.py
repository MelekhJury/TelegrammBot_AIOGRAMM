import sqlite3 as sq
from create import dp
import types

from handlers.create import bot

def sql_start():
    global base, cursor
    base = sq.connect("Группа.bd")
    cursor = base.cursor()
    if base:
        print("Подключение к базе данных Студентов - ОК")
    base.execute('''CREATE TABLE IF NOT EXISTS Студенты (id_student INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                         student    TEXT NULL)''')
    base.commit()

    if base:
        print("Подключение к базе ДЗ - ОК")
    base.execute('''CREATE TABLE IF NOT EXISTS ДЗ (id_home      INTEGER PRIMARY KEY AUTOINCREMENT ,
                                                   home         TEXT NULL,
                                                   id_student   INTEGER)''')
    base.commit()

async def sql_read():
    return cursor.execute(' SELECT * FROM Студенты student ').fetchall()

async def sql_read_home(data):
    return cursor.execute("SELECT home FROM ДЗ WHERE id_student == ?", (data,)).fetchall()


async def sql_add_stud_command(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO Студенты (student) VALUES(?)', tuple(data.values()))
        base.commit()

async def sql_add_home_command(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO ДЗ (home, id_student) VALUES(?,?)', tuple(data.values()))
        base.commit()

async def sql_delete_command(data):
    cursor.execute("DELETE FROM Студенты WHERE id_student == ?", (data,))
    cursor.execute("DELETE FROM ДЗ WHERE id_student == ?", (data,))
    base.commit()
