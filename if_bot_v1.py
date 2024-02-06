import telebot
import sqlite3
from datetime import datetime

bot = telebot.TeleBot('6277074360:AAFc43T6H8s3n6xJYox430lVkDlUv1t0fyo')
date = None
name = None
sum = None
id = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('if_bot.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Base_7 (id INTEGER, date TEXT, name TEXT, sum TEXT)""")
    conn.commit()
    cur.close()
    conn.close()

    current_datetime = datetime.now()
    current_datetime1 = current_datetime.strftime("%d-%m-%Y- %H:%M:%S")

    text1 = "Приветствую! Сейчас: "
    text2 = "Введите наименование выполненной затраты:"
    bot.send_message(message.chat.id, f"{text1}{current_datetime1} \n{text2}")

    global date
    date = current_datetime1
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите потраченную сумму на затрату:')
    bot.register_next_step_handler(message, user_sum)


def user_sum(message):
    global sum
    global id
    sum = message.text.strip()
    id = message.chat.id
    conn = sqlite3.connect('if_bot.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO  Base_7 (id, date, name, sum) VALUES(?,?,?,?);", (id, date, name, sum))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Сохранённые данные', callback_data='date'))
    bot.send_message(message.chat.id, 'Данные успешно сохранены!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callbeck(call):
    conn = sqlite3.connect('if_bot.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM Base_7')
    base = cur.fetchall()

    into = ''
    for el in base:
        into += f'Дата произведённых затрат: {el[1]}, Наименование затрат: {el[2]}, Сумма на затраты: {el[3]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, into)


@bot.message_handler(commands=['inf'])
def user_inf(message):
    bot.send_message(message.chat.id,
                     'Привет! \nДанный бот предназначен для записи, хранения и обработки данных. В частности, я его использую для хранения данных о текущих затратах. \nКоманды бота: \n  /start - бот начинает свою работу; \n  /inf - выводит это сообщение')


bot.polling(none_stop=True)
