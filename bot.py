import re
import random
from movies import movies
from genres import genres_map
from telegram_bot import TelegramBot

# Создаем нового телеграм бота
bot = TelegramBot('1834437618:AAFlQzOQXz_draeSv1rx03XwR2XaXggtyjg')


# Функция приветствия пользователя и вывод кнопок с доступными жанрами фильмов
def hello():
    bot.send_reply(f'Привет {bot.user_name}!')
    bot.add_buttons('Напиши мне любой год или выбери жанр, а я подберу тебе фильм на вечер ;)', genres_map)


# Функция подбора фильма
def get_movie():
    filtered_movies = movies
    message = bot.message.lower()

    if bot.update.callback_query:
        genre = bot.update.callback_query.data
        filtered_movies = list(filter(lambda m: genre in m['genres'], filtered_movies))

    year = re.findall('\\d{4}|$', message)[0]
    if year and 1900 <= int(year) <= 2018:
        filtered_movies = list(filter(lambda m: m['year'] == int(year), filtered_movies))

    movie = filtered_movies[random.randint(0, len(filtered_movies)-1)]
    bot.send_reply(f'Предлагаю посмотреть фильм {movie["title"]} ({movie["year"]})')
    if len(movie["cast"]) > 0:
        bot.send_reply(f'Там главные роли играют {", ".join(movie["cast"])}')


# Добавляем три разных обработчика событий
bot.add_command_handler('start', hello)  # для команды /start
bot.add_message_handler(get_movie)  # для любых сообщений
bot.add_query_handler(get_movie)  # для нажатия на кнопки с жанрами

# Непосредственно запускаем бота
bot.start()
