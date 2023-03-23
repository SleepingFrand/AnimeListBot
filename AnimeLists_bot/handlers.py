import telebot
from config import API_TOKEN_BOT, HELP_TXT, START_TXT

bot = telebot.TeleBot(API_TOKEN_BOT)

# обрабатываем только CallbackQuery с данными, начинающимися на "Ссылка:"
@bot.callback_query_handler(func=lambda call: CallBack_type(call.data, 'url-find'))
def start_callback(call):
    data = json.loads(call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, "jut.su" + data['url'])

####################################################

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=START_TXT)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text=HELP_TXT)

handlers = bot.message_handler
