import telebot
import callbacks  # Импортируем модуль с колбеками
import content_types  # Импортируем модуль с content_types
import commands  # Импортируем модуль с логикой команд
import sqlite3
import background

from telebot import types

#  Главное меню бота
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add(types.KeyboardButton('Моя стата'), types.KeyboardButton('Стата чата'),
                    types.KeyboardButton('Команды'), types.KeyboardButton('Игры'))

tg_token = 'ABOBA'

bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def start_bot(message):
    commands.start_message(message)


@bot.message_handler(commands=['help'])
def main_help_message(message):
    commands.help_message(message)


@bot.message_handler(commands=['based'])
def create_base(message):
    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    user_id = message.from_user.id
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cur.fetchone()

    if existing_user:
        bot.send_message(message.chat.id, 'Чел, ты уже базированный. Куда тебе второй раз?')
        with open('baza.gif', 'rb') as gif_antibase:
            bot.send_animation(message.chat.id, gif_antibase)

    else:
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                username TEXT,
                                name TEXT,
                                pass TEXT,
                                points INTEGER DEFAULT 0
                            )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS warnings(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    chat_id INTEGER,
                                    username TEXT
                                )''')

        conn.commit()

        bot.send_message(message.chat.id, '😎🤙Оууу мэн, ты зареган в базу шлёп.🐈', reply_markup=main_markup)
        with open('babza_main.gif', 'rb') as gif_base:
            bot.send_animation(message.chat.id, gif_base)

        bot.register_next_step_handler(message, user_name)

    cur.close()
    conn.close()


def user_name(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else 'govno'
    name = message.from_user.first_name

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (user_id, username, name, pass) VALUES (?, ?, ?, ?)",
                (user_id, username, name, ''))
    conn.commit()

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, f'Данные сохранены:\nИмя - {name}\nUsername - {username}')


@bot.message_handler(commands=['users'])
def main_get_users(message):
    commands.get_users(message)


@bot.message_handler(commands=['selfdata'])
def main_self_data(message):
    commands.self_data(message)


@bot.message_handler(commands=['warn'])
def main_warn_user(message):
    commands.warn_user(message)


@bot.message_handler(commands=['unwarn'])
def main_unwarn_user(message):
    commands.unwarn_user(message)


@bot.message_handler(commands=['mute'])
def main_mute_user(message):
    commands.mute_user(message)


@bot.message_handler(commands=['unmute'])
def main_unmute_user(message):
    commands.unmute_user_all(message)


@bot.message_handler(commands=['kick'])
def main_kick_user(message):
    commands.kick_user(message)


@bot.message_handler(commands=['fish'])
def main_fishing(message):
    user_id = message.from_user.id
    commands.fishing(message, user_id)


@bot.message_handler(commands=['rock'])
def rock_game(message):
    commands.play(message)


@bot.message_handler(commands=['random'])
def random_game(message):
    commands.start_game(message)


@bot.message_handler(commands=['gift'])
def give_points(message):
    commands.give_gift(message)


@bot.message_handler(commands=['grinch'])
def get_points_main(message):
    commands.get_points(message)


@bot.message_handler(content_types=['new_chat_members'])
def main_new_memeber(message):
    content_types.welcome_new_members(message)


@bot.message_handler(content_types=['left_chat_member'])
def main_left_member(message):
    content_types.farewell_member(message)


@bot.message_handler(content_types=['text'])
def main_text_message(message):
    content_types.text_message(message)


@bot.callback_query_handler(func=lambda call: call.data in ['камень', 'ножницы', 'бумага'])
def main_callback_rps(call):
    callbacks.callback_rps(call)


@bot.callback_query_handler(func=lambda call: True)
def inline_buttons(call):
    callbacks.handle_inline_buttons(call)

background.keep_alive()

bot.polling(none_stop=True)
