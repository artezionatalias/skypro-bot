import re
import random
from movies import movies
from telegram_bot import TelegramBot

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


bot = TelegramBot('1834437618:AAFlQzOQXz_draeSv1rx03XwR2XaXggtyjg')


def hello():
    bot.send_reply(f'Привет {bot.user_name}!')
    bot.send_reply('Напиши мне любой год или жанр, а я выберу тебе фильм на вечер ;)')
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
             InlineKeyboardButton("Option 2. Long text here. Long text here. Long text here.", callback_data='2'), 
             InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.update.message.reply_text('Please choose:', reply_markup=reply_markup)

def get_movie():
    query = bot.update.callback_query
    print(bot.update)
    print(query)
    filtered_movies = movies
    message = bot.message.lower()

    year = re.findall('\\d{4}|$', message)[0]
    if year and 1900 <= int(year) <= 2018:
        filtered_movies = list(filter(lambda movie: movie['year'] == int(year), filtered_movies))

    movie = filtered_movies[random.randint(0, len(filtered_movies)-1)]
    print(movie)
    bot.send_reply(f'Предлагаю посмотреть фильм {movie["title"]} ({movie["year"]})')
    if len(movie["cast"]) > 0:
        bot.send_reply(f'Там главные роли играют {", ".join(movie["cast"])}')


bot.add_command_handler('start', hello)
bot.add_message_handler(get_movie)
bot.add_query_handler(get_movie)

bot.start()
