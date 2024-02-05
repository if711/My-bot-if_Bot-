import telebot
import sqlite3
from datetime import datetime

bot = telebot.TeleBot('6277074360:AAFc43T6H8s3n6xJYox430lVkDlUv1t0fyo')
dt = None
n = None

@bot.message_handler(commands=['start'])
def start(message):
    c = sqlite3.connect('if_bot.db')
    cu = c.cursor()

    cu.execute("""CREATE TABLE IF NOT EXISTS Base_7 (date TEXT, name TEXT, sum TEXT)""")
    c.commit()
    cu.close()
    c.close()

    current_datetime = datetime.now()
    current_datetime1 = current_datetime.strftime("%d-%m-%Y- %H:%M:%S")

    text1 = "Приветствую! Сейчас: "
    text2 = "Введите наименование выполненной затраты:"
    bot.send_message(message.chat.id, f"{text1}{current_datetime1} \n{text2}")

    global dt
    dt = current_datetime1
    bot.register_next_step_handler(message, user_n)

def user_n(message):
    global n
    n = message.text.strip()
    bot.send_message(message.chat.id, 'Введите потраченную сумму на затрату:')
    bot.register_next_step_handler(message, user_s)

def user_s(message):
    sum = message.text.strip()
    c = sqlite3.connect('if_bot.db')
    cu = c.cursor()

    cu.execute ("INSERT INTO Base_7 (date, name, sum) VALUES ('%s', '%s', '%s')" % (dt, n, sum))
    c.commit()
    cu.close()
    c.close()

    bot.send_message(message.chat.id, 'Данные успешно сохранены!')



bot.polling(none_stop=True)
