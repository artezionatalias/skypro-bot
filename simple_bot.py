from telegram_bot import TelegramBot


bot = TelegramBot('YOUR TOKEN HERE')


def hello():
    bot.send_reply(f'Привет {bot.user_name}!')


bot.add_command_handler('start', hello)


bot.start()
