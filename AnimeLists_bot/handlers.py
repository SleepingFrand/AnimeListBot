import telebot
from config import API_TOKEN_BOT, HELP_TXT, START_TXT

bot = telebot.TeleBot(API_TOKEN_BOT)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=START_TXT)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text=HELP_TXT)

# Список обработчиков
handlers = bot.handlers
