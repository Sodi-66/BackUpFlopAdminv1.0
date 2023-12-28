import telebot
from telebot import types
import time
import sqlite3
import random
import utils
from config import main_markup, bot
from utils import user_name, short_mute
import config


def start_message(message):

    first_name = message.from_user.first_name

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Написать автору', url='https://t.me/tiltyxa'))

    bot.send_message(message.chat.id, f'Привет, *{first_name}*!😸Админ-шлёпа с функционалом админа позволяет легко '
                                      'мутить, банить,'' ограничивать доступ  в вашем чате. 🐱Автоматически мутит за'
                                      'определённые мут-слова, выдаёт предупреждения, добалвяет несколько забавных '
                                      'игр в вашу группу'' и другое. 🐈‍⬛ Для корректной работы бота подключите его к '
                                      'своей беседе. Введите команду */help* 🆘 для того, чтобы узнать список всех '
                                      'команд.\n*Для связи с автором - @tiltyxa*', reply_markup=keyboard,
                     parse_mode='Markdown')

    with open('hi_floppa.jpg', 'rb') as image_hi:
        bot.send_photo(message.chat.id, image_hi)


# СОЗДАНИЕ БАЗЫ ДАННЫХ - ДВЕ ТАБЛИЦЫ: ДАННЫЕ О ПОЛЬЗОВАТЕЛЯХ И ТАБЛИЦА О ПРЕДУПРЕЖДЕНИЯХ ПОЛЬЗОВАТЕЛЯ.
def create_base(message):

    first_name = message.from_user.first_name

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    user_id = message.from_user.id
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cur.fetchone()

    if existing_user:
        bot.send_message(message.chat.id, f'*{first_name}*, ты уже базирован(а)😎🤙. Куда тебе второй раз❓',
                         reply_markup=main_markup, parse_mode='Markdown')
        with open('baza.gif', 'rb') as gif_antibase:
            bot.send_animation(message.chat.id, gif_antibase)

    else:
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                username TEXT,
                                name TEXT,
                                pass TEXT,
                                points INTEGER DEFAULT 0,
                                level INTEGER DEFAULT 0
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


def get_users(message):

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("SELECT users.*, COUNT(warnings.id) FROM users LEFT JOIN warnings ON users.user_id = warnings.user_id "
                "GROUP BY users.id")
    users_data = cur.fetchall()

    conn.close()

    if users_data:
        response = 'Список чатеров📋: \n'
        for user in users_data:
            response += f'\nUser 🆔: {user[0]}\nUsername: {user[2]}👨‍🦰\nИмя: {user[3]}🧑\nПельмени: {user[5]}🥟' \
                        f'\nКоличество предупреждений: {user[7]}⚠️\nУровень: {user[6]}😼\n'
    else:
        response = 'База шлёп к сожалению пуста.🤷'

    bot.send_message(message.chat.id, response)


def self_data(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = cur.fetchone()

    if user_data:
        warnings_count = cur.execute("SELECT COUNT(*) FROM warnings WHERE user_id = ?", (user_id,)).fetchone()[0]
        user_level = user_data[6]  # Используйте актуальный индекс для столбца level

        response = (f'User 🆔: {user_data[0]}\nUsername: {user_data[2]}👨‍🦰\nИмя: {user_data[3]}🧑'
                   f'\nПельмени: {user_data[5]}🥟'f'\nКоличество предупреждений: {warnings_count}⚠️'
                   f'\nУровень: {user_level}😼')

    else:
        response = 'Вас нет в базе данных.😕\nВведите команду /based'

    conn.close()

    bot.send_message(message.chat.id, response)
    with open('self.gif', 'rb') as gif_self_data:
        bot.send_animation(message.chat.id, gif_self_data)


def help_message(message):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Написать автору', url='https://t.me/tiltyxa'))

    bot.send_message(message.chat.id, '*СПИСОК ВСЕХ КОМАНД📋:*\n\n*/kick* - кикнуть участника беседы.👊'
                                      'Применяется в ответ на сообщение чатера.🧍‍♂️\n*/mute* n - замутить участника '
                                      'беседы.🤐 Вместо n количест-во минут. По умолчанию 60.⏰ Применяется в ответ'
                                      ' на сообщение чатера.🧍‍♂️\n*/unmute* - размутить участника беседы🚫🤐'
                                      '. Применяется в ответ на сообщение чатера.🧍‍♂️\n*/selfdata* - Для просмотра своей'
                                      ' статистики.😎📋\n*/users* - для просмотра статистики по чату.💬📋\n*/warn* - '
                                      'выдать предупреждение.⚠️\n*/unwarn* - снять предупреждения.🚫⚠️\n\n*/random*'
                                      ' - игра "угадай число".🤔🔢\n*/rock* - Камень ножницы бумага.🥌✂️📄\n*/fish*'
                                      ' - игра "рыбалка".🎣\n\n*/based* - получить доступ к очкам, играм и т.д.🐈🖥',
                     parse_mode='Markdown', reply_markup=keyboard)

    with open('floppa_help.jpg', 'rb') as image_help:
        bot.send_photo(message.chat.id, image_help)


def warn_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        firstname_user = message.reply_to_message.from_user.first_name

        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

        if sender_status == 'administrator' or sender_status == 'creator':
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, 'Выдать предупреждение святейшему админу нельзя. Поэтому *пошёл нЭхуй!* 😡',
                             parse_mode='Markdown')
                with open('floppa_no.jpg', 'rb') as image_no:
                    bot.send_photo(message.chat.id, image_no)
            else:
                conn = sqlite3.connect('personal.sql')
                cur = conn.cursor()

                cur.execute("INSERT INTO warnings (user_id, chat_id, username) VALUES (?, ?, ?)",
                            (user_id, chat_id, username))
                conn.commit()

                utils.point_messages_minus(message.reply_to_message)

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('Написать автору', url='https://t.me/tiltyxa'))
                bot.send_message(chat_id,
                             f'Пользователь {firstname_user} получил предупреждение!'
                             f'\n*Введите команду /selfdata* , чтобы узнать сколько у вас предупреждений.⚠️',
                                 reply_markup=keyboard, parse_mode='Markdown')
                utils.point_messages_minus_twenty(message.reply_to_message)
                with open('cry.gif', 'rb') as image_warn:
                    bot.send_animation(message.chat.id, image_warn)

                warnings_count = cur.execute("SELECT COUNT(*) FROM warnings WHERE user_id = ?", (user_id,)).fetchone()[
                    0]
                if warnings_count >= 3:
                    bot.send_message(chat_id, 'Вы получили 3 предупреждения.⚠️ *Получите мут, сука.*🤐',
                                     parse_mode='Markdown')
                    short_mute(message.reply_to_message)

                conn.close()

        else:
            bot.reply_to(message, '*Вы не админ*, вам запрещено пользоваться такими командами. 🚫',
                         parse_mode='Markdown')
            with open('floppa_no.jpg', 'rb') as image_no:
                bot.send_photo(message.chat.id, image_no)

    else:
        bot.reply_to(message, 'Эта команда должна быть использована *в ответ на сообщение чатера*🚫‼️',
                     parse_mode='Markdown')
        with open('floppa_sadge.jpg', 'rb') as image_sadge:
            bot.send_photo(message.chat.id, image_sadge)


def unwarn_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        firstname_user = message.reply_to_message.from_user.first_name

        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

        if sender_status == 'administrator' or sender_status == 'creator':
            conn = sqlite3.connect('personal.sql')
            cur = conn.cursor()

            cur.execute("DELETE FROM warnings WHERE user_id = ?", (user_id,))
            conn.commit()

            bot.send_message(chat_id, f'Предупреждения *{firstname_user}* сброшены.🚫⚠️', parse_mode='Markdown')
            with open('happy.jpg', 'rb') as image_resent:
                bot.send_photo(message.chat.id, image_resent)

            conn.close()

        else:
            bot.reply_to(message, '*Вы не админ*, вам запрещено пользоваться такими командами. 🚫',
                         parse_mode='Markdown')
            with open('floppa_no.jpg', 'rb') as image_no:
                bot.send_photo(message.chat.id, image_no)

    else:
        bot.reply_to(message, 'Эта команда должна быть использована *в ответ на сообщение чатера*🚫‼️',
                     parse_mode='Markdown')
        with open('floppa_sadge.jpg', 'rb') as image_sadge:
            bot.send_photo(message.chat.id, image_sadge)


def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        firstname_user = message.reply_to_message.from_user.first_name

        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

        if sender_status == 'administrator' or sender_status == 'creator':
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, '*Вы пытаетесь кикнуть админа.* Поэтому идите нахуй, мистер‼️ ',
                             parse_mode='Markdown')
                with open('floppa_no.jpg', 'rb') as image_no:
                    bot.send_photo(message.chat.id, image_no)
            else:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f'Чатер *{firstname_user}* был казнён нахуй с позором. 💀',
                             parse_mode='Markdown')
                with open('floppa_strike.jpg', 'rb') as image_kick:
                    bot.send_photo(message.chat.id, image_kick)
        else:
            bot.reply_to(message, '*Вы не админ*, вам запрещено пользоваться такими командами. 🚫',
                         parse_mode='Markdown')
            with open('floppa_no.jpg', 'rb') as image_no:
                bot.send_photo(message.chat.id, image_no)
    else:
        bot.reply_to(message, 'Эта команда должна быть использована *в ответ на сообщение чатера*🚫‼️',
                     parse_mode='Markdown')
        with open('floppa_sadge.jpg', 'rb') as image_sadge:
            bot.send_photo(message.chat.id, image_sadge)


def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        firstname_user = message.reply_to_message.from_user.first_name

        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status
        user_status = bot.get_chat_member(chat_id, user_id).status

        if sender_status == 'administrator' or sender_status == 'creator':
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, 'Вы сука пытаетесь замутить админа. Поэтому *пошёл нЭхуй!* 😡',
                             parse_mode='Markdown')
                with open('big-floppa.gif', 'rb') as gif_nahuy:
                    bot.send_animation(message.chat.id, gif_nahuy)
            else:
                duration = 60
                arguments = message.text.split()[1:]
                if arguments:
                    try:
                        duration = int(arguments[0])
                    except ValueError:
                        bot.send_message(message.chat.id, 'Некорректно введено кол-во минут. ⏰')
                        return
                    if duration < 1:
                        bot.send_message(message.chat.id, 'Некорректно введено кол-во минут *(меньше минуты)*. ⏰',
                                         parse_mode='Markdown')
                        return
                    if duration > 1440:
                        bot.send_message(message.chat.id, 'Некорректно введено кол-во минут *(Нельзя замутить более чем '
                                                          'на день)*. ⏰', parse_mode='Markdown')
                        return

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton('Написать админу какой он хуесос', url='https://t.me/tiltyxa'))

                bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
                bot.send_message(message.chat.id, f'Завалил еблище, *{firstname_user}*‼️ Замучен на {duration} минут‼️ ',
                                 reply_markup=keyboard, parse_mode='Markdown')
                with open('floppa_mute.gif', 'rb') as gif_mute:
                    bot.send_animation(message.chat.id, gif_mute)
                utils.point_messages_minus_200(message)

        else:
            bot.reply_to(message, '*Вы не админ*, вам запрещено пользоваться такими командами. 🚫',
                         parse_mode='Markdown')
            with open('floppa_no.jpg', 'rb') as image_no:
                bot.send_photo(message.chat.id, image_no)

    else:
        bot.reply_to(message, 'Эта команда должна быть использована *в ответ на сообщение чатера*🚫‼️',
                     parse_mode='Markdown')
        with open('floppa_sadge.jpg', 'rb') as image_sadge:
            bot.send_photo(message.chat.id, image_sadge)


def unmute_user_all(message):

    if message.reply_to_message:

        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        firstname_user = message.reply_to_message.from_user.first_name

        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status

        if sender_status == 'administrator' or sender_status == 'creator':

            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_other_messages=True,
                                     can_send_media_messages=True, can_add_web_page_previews=True,
                                     can_pin_messages=True, can_invite_users=True, can_change_info=True,
                                     can_send_polls=True)

            bot.reply_to(message, f'Чатер *{firstname_user}* размучен. Следи за базаром.👺 ',
                         parse_mode='Markdown')
            with open('floppa_free.gif', 'rb') as gif_free:
                bot.send_animation(message.chat.id, gif_free)
        else:

            bot.reply_to(message, '*Вы не админ*, вам запрещено пользоваться такими командами. 🚫',
                         parse_mode='Markdown')
            with open('floppa_no.jpg', 'rb') as image_no:
                bot.send_photo(message.chat.id, image_no)
    else:
        bot.reply_to(message, 'Эта команда должна быть использована *в ответ на сообщение чатера*🚫‼️',
                     parse_mode='Markdown')
        with open('floppa_sadge.jpg', 'rb') as image_sadge:
            bot.send_photo(message.chat.id, image_sadge)


def start_game(message):
    chat_id = message.chat.id
    config.chat_states[chat_id] = {'guessing_number': random.randint(1, 20)}
    bot.send_message(chat_id, 'Я загадал число *от 1 до 20*. Попробуй угадать! 🤓', parse_mode='Markdown')


def play(message):
    user_id = message.from_user.id

    # Проверяем, была ли предыдущая игра и прошло ли 15 секунд с момента последней игры
    if user_id in config.last_play_time_rps and time.time() - config.last_play_time_rps[user_id] < 15:
        bot.send_message(message.chat.id, "*Чел, подожди немного* перед следующей игрой.👺",
                         parse_mode='Markdown')
        return

    inline_markup = utils.create_rps_inline_markup()
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие😼:", reply_markup=inline_markup)

    # Обновляем время последней игры для данного пользователя
    config.last_play_time_rps[user_id] = time.time()


def fishing(message, user_id):

    # Проверяем, была ли предыдущая игра и прошло ли 20 секунд с момента последней игры
    if user_id in config.last_play_time_fish and time.time() - config.last_play_time_fish[user_id] < 20:
        bot.reply_to(message, "*Чел, подожди немного* перед следующей игрой.👺", parse_mode='Markdown')
        return

    # Рандомно определяем, рыбу или мусор пользователь поймал
    if random.random() < 0.57:  # 57% вероятность поймать рыбу
        caught_item = random.choice(config.fishes)
        if caught_item == 'Золотая рыба🐠':
            bot.send_message(message.chat.id, f"Вы поймали *{caught_item}*! Шлёпа гордится тобой. 😼 Держи свои 20 пельменей. ⬆️✅🥟",
                         parse_mode='Markdown')
            utils.point_messages_plus_twenty(user_id)
        elif caught_item == 'Жёлтая рыба🐡':
            bot.send_message(message.chat.id, f"Вы поймали *{caught_item}*! Шлёпа гордится тобой. 😼 Держи свои 10 пельменей. ⬆️✅🥟",
                         parse_mode='Markdown')
            utils.point_messages_plus_ten(user_id)
        elif caught_item == 'Синяя рыба🐟':
            bot.send_message(message.chat.id, f"Вы поймали *{caught_item}*! Молодчик. 👏 Держи свои 5 пельменей. ⬆️✅🥟",
                         parse_mode='Markdown')
            utils.point_message_plus_five(user_id)
        elif caught_item == 'Коричневая рыба🟫':
            bot.send_message(message.chat.id, f"Вы поймали *{caught_item}*! Нормас. 👌 Держи свои 2 пельменя.⬆️✅🥟",
                         parse_mode='Markdown')
            utils.point_messages_plus_two(user_id)

    else:
        caught_item = random.choice(config.trash)
        if caught_item == 'Бімба💣💥':
            bot.reply_to(message, f"Воу, чел! Ты поймал *{caught_item}*! Шлёпа выражает дизреспект! 😤 Заберите 20"
                                  f" пельменей у него! ❌⬇️🥟", parse_mode='Markdown')
            utils.point_messages_minus_twenty_fishing(user_id)
        elif caught_item == 'Пакеты🛍':
            bot.reply_to(message, f"Ты поймал *{caught_item}*! И зачем они мне? 😾 Заберите 10 пельменей у него! ❌⬇️🥟",
                         parse_mode='Markdown')
            utils.point_messages_minus_ten(user_id)
        elif caught_item == 'Банки🥫🥫':
            bot.reply_to(message, f"Ты поймал *{caught_item}*! Не повезло, они мне не нужны. 🐱 Заберите 6 пельменей "
                                  f"у него! ❌⬇️🥟", parse_mode='Markdown')
            utils.point_messages_minus_fishing(user_id)

    # Обновляем время последней игры для данного пользователя
    config.last_play_time_fish[user_id] = time.time()


