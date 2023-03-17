import json
import telebot
from telebot import types
from site_parser import jutsu
from site_parser import amine_url_lib

##################__ПЕРЕМЕННЫЕ__####################

bot = telebot.TeleBot('6269409208:AAGGRTV5V6kCYxih2tXM8RYDp1MRMu7ZQmY')
url = amine_url_lib['jutsu']

####################__ФАЙЛЫ__#######################

# Считываем файл с помощью -> /help
file_help = open('help.txt', 'r')
help_text = file_help.read()
file_help.close()

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

####################__ПАМЯТЬ_БОТА__#####################

anime_list_finded = dict()

####################__ФУНКЦИИ_БОТА__####################

# Обработчик базовых команд 
@bot.message_handler(commands=['start', 'help'])
def command_base(message):
    if message.text == "/start":
        NoneFunction(message)
    if message.text == "/help":
        bot.send_message(message.from_user.id, help_text)

# обрабатываем только CallbackQuery с данными, начинающимися на "Ссылка:"
@bot.callback_query_handler(func=lambda call: CallBack_type(call.data, 'url-find'))
def start_callback(call):
    data = json.loads(call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, "jut.su" + data['url'])

# Обработчик сообщений с текстом
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global anime_list_finded 

    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")

    # Если попросили чтото найти  ->  "Найди ...."
    elif message.text.lower().split()[0] == 'найди': 
        anime_list_finded = FindAnime(' '.join(message.text.lower().split()[1:]))
        reply = "Вот что я нашел на " + url[8:] + ":\n"
        for key in anime_list_finded:
            reply += key + '\n'
        bot.send_message(message.from_user.id, reply)

    # Информация о аниме
    elif message.text.lower() == 'выбрать':
        if len(anime_list_finded) > 0:
            markup = types.InlineKeyboardMarkup()
            for key, value in anime_list_finded.items():
                btn = types.InlineKeyboardButton(text=key, callback_data=json.dumps({'head':'url-find','url':value}))
                markup.add(btn)
            bot.send_message(message.chat.id, "Выбирай", reply_markup = markup)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)