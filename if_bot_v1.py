#Подключение необходимых библиотек
import telebot
import sqlite3
from datetime import datetime

#Подключение к боту через его индивидуальный ключ-токен, а также задание начальных значений глобальных переменных.
bot = telebot.TeleBot('6277074360:AAFc43T6H8s3n6xJYox430lVkDlUv1t0fyo')
date = None
name = None
sum = None
id = None

#Команда "start" отвечает за начало работы бота, создаётся БД в sqlite3, регистрируется текущее время запроса, и спрашивается у пользователя наименование выполненной затраты.
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('if_bot.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Base_7 (id INTEGER, date TEXT, name TEXT, sum TEXT)""")
    conn.commit()
    cur.close()
    conn.close()

    #Автоматическое считывание даты и времени запроса пользователя.
    current_datetime = datetime.now()
    current_datetime1 = current_datetime.strftime("%d-%m-%Y- %H:%M:%S")

    text1 = "Приветствую! Сейчас: "
    text2 = "Введите наименование выполненной затраты:"
    bot.send_message(message.chat.id, f"{text1}{current_datetime1} \n{text2}")

    global date
    date = current_datetime1
    bot.register_next_step_handler(message, user_name)

#Сохраняется информация о наименовании затраты, спрашивается сумма на произведённую затрату.
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите потраченную сумму на затрату:')
    bot.register_next_step_handler(message, user_sum)

#Сохраняется информация о сумме на затрату, а также индивидуальный id пользователя, производившего запрос. Также сохраняются все ранее ввёдённые данные в БД sqlite3.
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

    #Создание кнопки "Сохранённые данные".
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Сохранённые данные',callback_data= 'date'))
    bot.send_message(message.chat.id, 'Данные успешно сохранены!', reply_markup=markup)

#Команда "del" отвечает за полную очистку данных в БД.
@bot.message_handler(commands=['del'])
def user_del(message):
    conn = sqlite3.connect('if_bot.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM Base_7')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Табличные данные успешно очищены!')

#Команда "data" отвечает повторый вывод кнопки с сохранёнными данными, и непосредственно ранее введённую информацию.
@bot.message_handler(commands=['data'])
def user_dat(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Сохранённые данные', callback_data='date'))
    bot.send_message(message.chat.id, 'Сохранённые данные:', reply_markup=markup)

#Отображение ранее ввёдённых данных, запуск производится с кнопки "Сохранённые данные".
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

    bot.send_message(call.message.chat.id,into)

#Функций "ing" отвечает за выпод первичной информации о возможностях бота, а также информацию о его функциях.
@bot.message_handler(commands=['inf'])
def user_inf(message):
    bot.send_message(message.chat.id, 'Доброго времени суток! \nДанный бот предназначен для записи, хранения и обработки данных. Код данного бота написан на языке Python. В качестве ячейки для хранения данных используется движок sqlite3. Одна из вариаций использования данного бота - использование для хранения данных о текущих затратах. \n Итак, давайте ознакомимся с функциями ботa: \n С помощью команды: \n  /start - бот начинает свою работу; \n  /del - выполняет полную очистку всех ранее введённых данных; \n  /data - выводит все ранее введённые данные; \n  /inf - выводит это сообщение. \n  Для удобства использования фукнций нажмите раздел "Меню". \n  : ) Удачи! ')


bot.polling(none_stop=True)
