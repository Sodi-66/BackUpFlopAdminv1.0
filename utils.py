import sqlite3
import time
from telebot import types
from config import bot


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

    bot.send_message(message.chat.id, f'*Данные сохранены*🎉:\nИмя - {name}\nUsername - {username}',
                     parse_mode='Markdown')


def short_mute(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    firstname_user = message.from_user.first_name
    user_status = bot.get_chat_member(chat_id, user_id).status

    if user_status == 'administrator' or user_status == 'creator':
        bot.reply_to(message, f'Вы сука *пытаетесь замутить админа*, {firstname_user}. Поэтому иди ты нахуй ' 
                     '🖕🏿😠', parse_mode='Markdown')
        with open('big-floppa.gif', 'rb') as gif_nahuy:
            bot.send_animation(message.chat.id, gif_nahuy)
    else:
        duration = 60

        bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration * 60)
        bot.reply_to(message, f'Завалил еблище, *{firstname_user}*!🤬 Замучен на *{duration} минуты*!🕞 ',
                     parse_mode='Markdown')
        with open('floppa_mute.gif', 'rb') as gif_mute:
            bot.send_animation(message.chat.id, gif_mute)


def update_levels(message):

    first_name = message.from_user.first_name

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("SELECT user_id, points, level FROM users")
    user_levels = cur.fetchall()

    for user_id, points, old_level in user_levels:
        new_level = 0
        level_cost = 100  # Стоимость для достижения первого уровня

        while points >= level_cost:
            new_level += 1
            level_cost += 85 + new_level * 100  # Увеличиваем цену для следующего уровня

        if new_level > old_level:
            bot.send_message(message.chat.id, f'Поздравляем, {first_name}!🥳 *Вы достигли нового уровня: {new_level}!*'
                             '\nШлёпа гордится тобой!🐈 Миску мятных пряников ему!🥣🍩\n➕1️⃣5️⃣ *к шлёпному рейтингу*',
                             parse_mode='Markdown')
            cur.execute("UPDATE users SET level = ? WHERE user_id = ?", (new_level, user_id))
            with open('vdacha!.gif', 'rb') as image_vdacha:
                bot.send_animation(message.chat.id, image_vdacha)

        elif new_level < old_level:
            bot.send_message(message.chat.id, f'{first_name.title()}, *ваш уровень уменьшился до: {new_level}.*😭 Ты '
                                              f'пал в глазах Шлёпы.😡\n➖1️⃣5️⃣ *к шлёпному рейтингу!*',
                             parse_mode='Markdown')
            cur.execute("UPDATE users SET level = ? WHERE user_id = ?", (new_level, user_id))

    conn.commit()
    conn.close()


def create_rps_inline_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Камень', callback_data='камень'),
               types.InlineKeyboardButton('Ножницы', callback_data='ножницы'),
               types.InlineKeyboardButton('Бумага', callback_data='бумага'))
    return markup


def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "Ничья!😾"
    elif (user_choice == 'камень' and bot_choice == 'ножницы') or \
            (user_choice == 'ножницы' and bot_choice == 'бумага') or \
            (user_choice == 'бумага' and bot_choice == 'камень'):
        return "Ты победил Шлёпу!😿"
    else:
        return "Шлёпа победил!😸"


def point_messages_plus_twenty(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 20 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_plus_two(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 2 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_message_plus_five(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 5 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_fishing(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 6 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 6 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_plus_ten_rps(user_id):
    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 10 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_ten_rps(user_id):
    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 10 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_plus_ten(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 10 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_twenty_fishing(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 20 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_twenty(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 20 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_ten(user_id):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 10 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_four(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 4 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_messages_minus_200(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points - 200 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()


def point_message_plus_fiveteen(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 15 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()