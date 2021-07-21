from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext


# Вспомогательная функция разбиения списка на подсписки
# Используем чтоб кнопки с жанрами фильмов выводились по три в ряд
def func_chunks_generators(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


class TelegramBot:
    # Конструктор класса, в котором мы создаем объект класса Updater и передаем ему токен
    def __init__(self, token: str):
        self.updater = Updater(token)
        self.update = None
        self.context = None
        self.user_name = ''
        self.message = ''

    # Стартуем наш телеграм бот и вызываем функцию idle() 
    # которая не дает нашему боту закрыться, а держит его все время в рабочем состоянии
    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    # Функция отправки ответного сообщения
    def send_reply(self, text: str):
        if self.update.message:
            self.update.message.reply_text(text)
        if self.update.callback_query:
            self.context.bot.send_message(chat_id=self.update.callback_query.message.chat_id, text=text)

    # Функция добавления кнопок
    def add_buttons(self, text: str, buttons):
        keyboard = []
        for btn in buttons:
            keyboard.append(InlineKeyboardButton(btn[1], callback_data=btn[0]))

        reply_markup = InlineKeyboardMarkup(list(func_chunks_generators(keyboard, 3)))
        self.update.message.reply_text(text, reply_markup=reply_markup)
    
    # Функция обертка для callback функции
    # сохраняет информацию о пользователе и сообщении и вызывает изначальную функцию
    def callback_fn(self, update: Update, context: CallbackContext, callback: callable):
        self.context = context
        self.update = update
        self.user_name = update.effective_user.first_name
        self.message = update.message.text if update.message else ''
        callback()

    # Функция по добавлению обработчика команд
    def add_command_handler(self, name: str, callback: callable):
        self.updater.dispatcher.add_handler(
            CommandHandler(name, lambda update, context: self.callback_fn(update, context, callback)))

    # Функция по добавлению обработчика сообщений
    def add_message_handler(self, callback: callable):
        self.updater.dispatcher.add_handler(
            MessageHandler(filters=Filters.update,
                           callback=lambda update, context: self.callback_fn(update, context, callback)))

    # Функция по добавлению обработчика запросов
    def add_query_handler(self, callback: callable):
        self.updater.dispatcher.add_handler(
            CallbackQueryHandler(lambda update, context: self.callback_fn(update, context, callback)))
