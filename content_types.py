import sqlite3
import utils
import commands
from telebot import types
from config import chat_states, main_markup
from config import bot

zelik = ['zelik', 'зелик', 'зеля', 'цандырь', 'цанга', 'слава цандырю']
stop_words = ['ты левак', 'левак', 'гоща лох', 'слава россии', 'гоша чмо', 'гоща чмо', 'гоша loh',
              'лох гоша', 'гоша левак']

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for new_member in message.new_chat_members:

        bot.send_message(message.chat.id, f'Ку блять,*{new_member.first_name}*, ебаный ты баклажан!🍆'
                                          '\n *Введи коанду /based* чтобы стать жоско базированным(ной).😎🤙'
                                          '\nВведи /help - чтобы узнать все команды.📋',parse_mode='Markdown')

        with open('hi_floppa.jpg', 'rb') as image_hi:
            bot.send_photo(message.chat.id, image_hi)


@bot.message_handler(content_types=['left_chat_member'])
def farewell_member(message):
    left_member = message.left_chat_member

    bot.send_message(message.chat.id, f'Пиздец!🤯 У нас потери! {left_member.first_name} покинул нас.😧')

    with open('floppa_sadge.jpg', 'rb') as image_sadge:
        bot.send_photo(message.chat.id, image_sadge)


@bot.message_handler(content_types=['text'])
def text_message(message):

    if message.text.strip().lower() == 'пельмени' or message.text.strip().lower() == 'пельмень':
        with open('Хорошие пельмени это очень вкусно (by DailyRay ♪).mp4', 'rb') as video_dumpling:
            bot.send_video(message.chat.id, video_dumpling)
        with open('floppa_dumpling.jpg', 'rb') as image_dumpling:
            bot.send_photo(message.chat.id, image_dumpling)
        bot.reply_to(message, '🥟*ХОРОШИЕ ПЕЛЬМЕНИ ЭТО ЕБАТЬ КАК ВКУСНО!*🥟', parse_mode='Markdown')

    if 'хуй' in message.text.strip().lower() or 'гош, кар' in message.text.strip().lower():
        with open('Шлепа сказал хуй.mp4', 'rb') as video_huy:
            bot.send_video(message.chat.id, video_huy)
        bot.reply_to(message, '*ХХХХХХХХХХХХУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ'
                              'УУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ'
                              'УУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ'
                              'УУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ'
                              'УУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ'
                              'УУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ'
                              'УУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙЙ*',
                     parse_mode='Markdown')

    if message.text.strip().lower() == 'привет' or message.text.strip().lower() == 'здарова' \
            or message.text.strip().lower() == 'ку':
        bot.reply_to(message, 'Здарова, чел! 👋😼')
        with open('floppa_hhuy.jpg', 'rb') as image_hhuy:
            bot.send_photo(message.chat.id, image_hhuy)

    if 'витя' in message.text.strip().lower() or 'юдин' in message.text.strip().lower():
        with open('Stive_Flopps.jpg', 'rb') as image_flopps:
            bot.send_photo(message.chat.id, image_flopps)

    if message.text.strip().lower() == 'гоша' or message.text.strip().lower() == 'гладыр':
        bot.reply_to(message, '😎Мега крутой чел.😎')
        with open('Goshagif.gif', 'rb') as gif_gosh:
            bot.send_animation(message.chat.id, gif_gosh)

    if message.text.strip().lower() == 'гоша лох' or 'шлёпа лох' in message.text.strip().lower():
        bot.reply_to(message, '🤬 Мама твой лох! Щэрсть йобанай. 🤬')

        utils.short_mute(message)
        utils.point_messages_minus_200(message)

    if message.text.strip().lower() == 'моя стата':
        commands.self_data(message)

    if message.text.strip().lower() == 'стата чата':
        commands.get_users(message)

    if message.text.strip().lower() == 'игры':
        markup_game = types.InlineKeyboardMarkup(row_width=2)
        markup_game.add(types.InlineKeyboardButton('Числа', callback_data='numbers'),
                        types.InlineKeyboardButton('КНБ', callback_data='rock_paper_scissors'),
                        types.InlineKeyboardButton('Рыбалка', callback_data='fishing'))
        bot.send_message(message.chat.id, "Выбери игру🎮:", reply_markup=markup_game)

    if message.text.strip().lower() == 'команды':
        commands.help_message(message)

    if message.text.strip().lower() == 'камень':
        bot.send_message(message.chat.id, 'Нет блять, бумага 📄', reply_markup=main_markup)

    if message.text.strip().lower() == 'ножницы':
        bot.send_message(message.chat.id, 'Нет блять, камень 🗿', reply_markup=main_markup)

    if message.text.strip().lower() == 'бумага':
        bot.send_message(message.chat.id, 'Нет блять, ножницы ✂️', reply_markup=main_markup)

    if 'губами' in message.text.strip().lower():
        bot.reply_to(message, '👄ГУБАМИ!💋')
        with open('gubanin.jpg', 'rb') as guba:
            bot.send_photo(message.chat.id, guba)

    def text_zelik(message):
        text = message.text.strip().lower()
        found = False

        for keyword in zelik:
            if keyword in text:
                found = True
                break

        if 'цандырь' in text or found:
            bot.send_message(message.chat.id, '*Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! '
                                              'Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! '
                                              'Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! '
                                              'Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! '
                                              'Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! Слава ЦАНДЫРЮ! '
                                              'Слава ЦАНДЫРЮ! *', parse_mode='Markdown')
            with open('zelik.jpg', 'rb') as zelya:
                bot.send_photo(message.chat.id, zelya)

    stop_words_check(message)
    text_zelik(message)
    point_messages(message)
    play_game(message)


def stop_words_check(message):
    text = message.text.strip().lower()
    found = False

    for keyword in stop_words:
        if keyword in text:
            found = True
            break

    if 'шлепа лох' in text or found:
        bot.send_message(message.chat.id, '*Я те ща еблет сломаю сука, выбирай выражения на! *',
                         parse_mode='Markdown')

        utils.short_mute(message)


@bot.message_handler(func=lambda message: True)
def play_game(message):
    chat_id = message.chat.id
    if chat_id in chat_states:
        guessed_number = chat_states[chat_id]['guessing_number']
        try:
            guess = int(message.text)
            if guess == guessed_number:
                bot.send_message(chat_id, "Поздравляю! *Ты угадал число!* 👏 +15 пельменей этому челу! ⬆️✅🥟",
                                 parse_mode='Markdown')
                utils.point_message_plus_fiveteen(message)
                with open('floppa_dumpling.jpg', 'rb') as image_dumpling:
                    bot.send_photo(message.chat.id, image_dumpling)
                del chat_states[chat_id]
            elif guess < guessed_number:
                bot.send_message(chat_id, "Попробуй больше! -4 пельменя ❗⬇️🥟")
                utils.point_messages_minus_four(message)
            else:
                bot.send_message(chat_id, "Попробуй меньше! -4 пельменя ❗️⬇️🥟")
                utils.point_messages_minus_four(message)
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, *введите число.* 😾❗️", parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def point_messages(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('personal.sql')
    cur = conn.cursor()

    cur.execute("UPDATE users SET points = points + 1 WHERE user_id=?", (user_id,))
    conn.commit()

    conn.close()

    utils.update_levels(message)  # Вызываем функцию для обновления уровней


