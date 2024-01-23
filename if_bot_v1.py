import telebot
import sqlite3

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

    bot.send_message(message.chat.id, 'Приветствую! Готов к работе, введите пожалуйста сегодняшнюю дату:')
    bot.register_next_step_handler(message,user_dt)

def user_dt(message):
    global dt
    dt = message.text.strip()
    bot.send_message(message.chat.id, 'Введите наименование выполненной затраты:')
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

