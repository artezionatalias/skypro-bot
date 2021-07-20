from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class TelegramBot():
    # Конструктор класса, в котором мы создаем объект класса Updater и передаем ему токен
    def __init__(self, token:str):
        self.updater = Updater(token)

    # Стартуем наш телеграм бот и вызываем функцию idle() 
    # которая не дает нашему боту закрыться, а держит его все время в рабочем состоянии
    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    # Функция отправки ответного сообщения
    def send_reply(self, text:str):
        self.update.message.reply_text(text)
    
    # Функция обертка для callback функции
    # сохраняет информацию о пользователе и сообщении и вызывает изначальную функцию
    def callbackFn(self, update: Update, callback:callable):
        self.update = update
        self.user_name = update.effective_user.first_name
        self.message = update.message.text
        callback()

    # Функция по добавлению обработчика команд
    def add_command_handler(self, name:str, callback:callable):
        #lambda event, args=args: self.do_something(event, args)
        self.updater.dispatcher.add_handler(CommandHandler(name, lambda update, context: self.callbackFn(update, callback)))

    # Функция по добавлению обработчика сообщений
    def add_message_handler(self, callback:callable):
        self.updater.dispatcher.add_handler(MessageHandler(filters=Filters.update, callback=lambda update, context: self.callbackFn(update, callback)))
