import telebot
from telebot import types
from config import API_TOKEN_BOT, HELP_TXT, START_TXT
import json
from utils import Anime, Anime_data, GetListFromData
from site_parser import jutsu
from site_parser import amine_url_lib
import time

bot = telebot.TeleBot(API_TOKEN_BOT)
url = amine_url_lib['jutsu']

anime_info:dict[int, Anime] = {}
last_interaction_time:dict[int, float] = {}

##################################################

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

def UpdateTime(id):
    global last_interaction_time
    # обновляем время последнего общения при получении каждого нового сообщения
    last_interaction_time[id] = time.time()

####################################################

# 
def find_callback_back(chat_id, url):
    """
    Формирует основное информативное сообщение с информацией по аниме 
    """
    global Anime_data
    global anime_info

    added_list = False
    index_list = 0

    for i, item in enumerate(Anime_data[chat_id]):
        if item.title == anime_info[chat_id].title:
            anime_info[chat_id].watched = Anime_data[chat_id][i].watched
            added_list = True
            index_list = i

    markup = types.InlineKeyboardMarkup()

    if added_list:
        if Anime_data[chat_id][index_list].watched < Anime_data[chat_id][index_list].episodes:
            markup.add(types.InlineKeyboardButton(text='просмотренно серий + 1', callback_data=json.dumps({'head':'an','v':4, 'id':index_list , 'url':url})))
            markup.add(types.InlineKeyboardButton(text='Ссылка на серию', callback_data=json.dumps({'head':'an','v':2})))
        
        if Anime_data[chat_id][index_list].watched > 0:
            markup.add(types.InlineKeyboardButton(text='просмотренно серий - 1', callback_data=json.dumps({'head':'an','v':5, 'id':index_list , 'url':url})))
        
        markup.add(types.InlineKeyboardButton(text='Удалить из списока', callback_data=json.dumps({'head':'an','v':3, 'id':index_list})))
        
    else:
        markup.add(types.InlineKeyboardButton(text='Добавить в список', callback_data=json.dumps({'head':'an','v':1, 'url':url})))
        markup.add(types.InlineKeyboardButton(text='Ссылка на серию', callback_data=json.dumps({'head':'an','v':2})))

    markup.add(types.InlineKeyboardButton(text='Отмена', callback_data=json.dumps({'head':'an','v':-1})))

    bot.send_message(chat_id, anime_info[chat_id].get_info_to_str(), reply_markup = markup)

#
def send_list(message, page=1):
    """
    Отправит пользователю сообщение с клавиатурой, содержащей список elements.
    Если длина списка больше 10 элементов, то список будет разделен на странички и
    добавлены кнопки для перелистывания вперед и назад.
    page - текущая страница (значение по умолчанию 1).
    """
    global Anime_data

    # Если список пустой
    if not Anime_data[message.chat.id]:
        bot.send_message(message.chat.id, "Список пуст")
        return

    # Вычисляем номера элементов, входящих в текущую страницу
    item_range = slice((page-1)*10, page*10)
    items_on_page = Anime_data[message.chat.id][item_range]

    # Создание клавиатуры кнопок со списком элементов
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for item in items_on_page:
        button = types.InlineKeyboardButton(text=item.title, callback_data='item_'+ '/' + item.site.split('/')[-2] + '/')
        keyboard.add(button)

    # Создание кнопок "вперед" и "назад" для переключения страниц
    back_button = types.InlineKeyboardButton(text="<<", callback_data="prev-page_{}".format(page))
    forward_button = types.InlineKeyboardButton(text=">>", callback_data="next-page_{}".format(page))
    
    #Если список находится на первой страницы, мы не хотим показывать кнопку "назад"
    if page != 1:
      keyboard.row(back_button)
    #Если список находится на последней странице, мы не хотим показывать кнопку "вперед"
    elif page != len(Anime_data[message.chat.id]) // 10 + 1:
      keyboard.row(forward_button)

    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id, "Список контента:", reply_markup=keyboard)

#############################################################

#
@bot.callback_query_handler(func=lambda call: call.data.startswith('prev-page_') or call.data.startswith('next-page_') or call.data.startswith('item_'))
def handle_callback_query(call):
    """
    Обрабатывает callback_query, отправляя следующую или предыдущую страницу или
    реагирует на выбор пользователя.
    """
    UpdateTime(call.message.chat.id)
    global Anime_data

    # Отделяем префикс и аргументы из callback_data
    prefix, argument = call.data.split("_", 1)

    # Переключение на следующую страницу списка
    if prefix == "next-page":
        page = int(argument)
        send_list(call.message, page=page+1)
        
    # Переключение на предыдущую страницу списка
    elif prefix == "prev-page":
        page = int(argument)
        send_list(call.message, page=page-1)
        
    # Обработка выбора пользователя
    elif prefix == "item":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        anime_info[call.message.chat.id] = jutsu.info_per_url(argument)
        find_callback_back(call.message.chat.id, argument)

# обрабатываем только CallbackQuery с данными 'head':'url-find'
@bot.callback_query_handler(func=lambda call: json.loads(call.data)['head'] == 'url-find')
def find_callback(call):
    UpdateTime(call.message.chat.id)
    global Anime_data
    global anime_info
    data = json.loads(call.data)
    anime_info[call.message.chat.id] = jutsu.info_per_url(data['url'])
    # Удаляем сообщение и отправляем другое
    bot.delete_message(call.message.chat.id, call.message.message_id)
    find_callback_back(call.message.chat.id, data['url'])

# обрабатываем только CallbackQuery с данными 'head':'an'
@bot.callback_query_handler(func=lambda call: json.loads(call.data)['head'] == 'an')
def anime_callback(call):
    """
    Обрабатывает нажатие кнопок в основной инфо панели
    """
    UpdateTime(call.message.chat.id)
    global Anime_data
    global anime_info
    data = json.loads(call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if data['v'] == 1:
        Anime_data[call.message.chat.id].append(anime_info[call.message.chat.id])
        find_callback_back(call.message.chat.id, data['url'])
    elif data['v'] == 2:
        mess = jutsu.get_url_episode(anime_info[call.message.chat.id].site, anime_info[call.message.chat.id].watched + 1)
        if mess == None:
            bot.send_message(call.from_user.id, 'Не могу найти серию(')
        else:
            bot.send_message(call.from_user.id, mess)
            Anime_data[call.message.chat.id][data['id']].watched += 1
    elif data['v'] == 3:
        Anime_data[call.message.chat.id].pop(data['id'])
        bot.send_message(call.from_user.id, 'Удалена из списка')
    elif data['v'] == 4:
        Anime_data[call.message.chat.id][data['id']].watched += 1
        find_callback_back(call.message.chat.id, data['url'])
    elif data['v'] == 5:
        Anime_data[call.message.chat.id][data['id']].watched -= 1
        find_callback_back(call.message.chat.id, data['url'])
    

####################################################

# Старт комманда
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=START_TXT)
    if message.chat.id not in Anime_data:
        Anime_data[message.chat.id] = []
    UpdateTime(message.chat.id)

# Помощь комманда
@bot.message_handler(commands=['help'])
def help(message):
    UpdateTime(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=HELP_TXT)

# Обработчик сообщений с текстом
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    UpdateTime(message.chat.id)

    GetListFromData(message.chat.id)

    anime_list_finded = dict()
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")

    # Если попросили чтото найти  ->  "Найди ...." || "Найти ...."
    elif message.text.lower().split()[0] == 'найди' or message.text.lower().split()[0] == 'найти': 
        anime_list_finded = FindAnime(' '.join(message.text.lower().split()[1:]))
        if len(anime_list_finded) > 0:
            markup = types.InlineKeyboardMarkup()
            for key, vue in anime_list_finded.items():
                btn = types.InlineKeyboardButton(text=key, callback_data=json.dumps({'head':'url-find','url':vue}))
                markup.add(btn)
            bot.send_message(message.chat.id, "Вот что я нашел на " + url[8:] + ":", reply_markup = markup)
    # Если попросили список -> "Список"
    elif message.text.lower().split()[0] == 'список':
        send_list(message)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")

# Копируем заголовки для main
handlers = bot.message_handler