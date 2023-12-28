import random
import utils
import config
import time
from commands import start_game, play, fishing
from config import bot


@bot.callback_query_handler(func=lambda call: call.data in ['камень', 'ножницы', 'бумага'])
def callback_rps(call):
    user_id = call.from_user.id

    # Проверяем, была ли предыдущая игра и прошло ли 15 секунд с момента последней игры
    if user_id in config.last_play_time_rps and time.time() - config.last_play_time_rps[user_id] < 15:
        bot.send_message(call.message.chat.id, "*Чел, подожди немного* перед следующей игрой.👺",
                         parse_mode='Markdown')
        return

    user_choice = call.data
    bot_choice = random.choice(['камень', 'ножницы', 'бумага'])
    result = utils.determine_winner(user_choice, bot_choice)

    bot.send_message(call.message.chat.id, f'*Твой выбор🤓:* {user_choice.capitalize()}\n'
                                            f'*Выбор Шлёпы😼:* {bot_choice.capitalize()}\n'
                                            f'*Результат🙀:* {result}\n\n',
                     parse_mode='Markdown')

    if result == "Ты победил Шлёпу!😿":
        utils.point_messages_plus_ten_rps(user_id)
    elif result == "Шлёпа победил!😸":
        utils.point_messages_minus_ten_rps(user_id)

    # Обновляем время последней игры для данного пользователя
    config.last_play_time_rps[user_id] = time.time()


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == 'numbers':
        start_game(call.message)
    elif call.data == 'rock_paper_scissors':
        play(call.message)
    elif call.data == 'fishing':
        fishing(call.message, call.from_user.id)
