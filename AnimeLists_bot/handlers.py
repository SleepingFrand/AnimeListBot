import telebot
from telebot import types
from config import API_TOKEN_BOT, HELP_TXT, START_TXT
import json
from utils import Anime, Anime_data
from site_parser import jutsu
from site_parser import amine_url_lib

bot = telebot.TeleBot(API_TOKEN_BOT)
url = amine_url_lib['jutsu']

############__ВСПОМОГАТЕЛЬНЫЕ_ФУНКЦИИ__#############

# Выбор активного сайта
def ChooseAnimeSite():
    site = 'jutsu'
    url = amine_url_lib[site]

# Поиск аниме по названию
def FindAnime(name: str) -> list[str]:
    anime_list = []

    # для jut.su
    if url == amine_url_lib['jutsu']:
        anime_list = jutsu.find_amime(name=name)

    return anime_list

# Функция заглушка
def NoneFunction(message):
    bot.reply_to(message, 'Прости, но пока я не могу отвечать на это, но совсем скоро научусь!')

#
def CallBack_type(data:str,type_name:str):
    data = json.loads(data)
    return data['head'] == type_name

####################################################

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

# Обработчик сообщений с текстом
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    anime_list_finded = dict()
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")

    # Если попросили чтото найти  ->  "Найди ...."
    elif message.text.lower().split()[0] == 'найди': 
        anime_list_finded = FindAnime(' '.join(message.text.lower().split()[1:]))
        if len(anime_list_finded) > 0:
            markup = types.InlineKeyboardMarkup()
            for key, value in anime_list_finded.items():
                btn = types.InlineKeyboardButton(text=key, callback_data=json.dumps({'head':'url-find','url':value}))
                markup.add(btn)
            bot.send_message(message.chat.id, "Вот что я нашел на " + url[8:] + ":", reply_markup = markup)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

handlers = bot.message_handler
