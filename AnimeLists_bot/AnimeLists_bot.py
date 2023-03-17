import telebot
from site_parser import jutsu

amine_url_lib = { 
    'jutsu' : 'https://jut.su/anime/'
    }

url = amine_url_lib['jutsu']

bot = telebot.TeleBot('6269409208:AAGGRTV5V6kCYxih2tXM8RYDp1MRMu7ZQmY')

file_help = open('help.txt', 'r')
help_text = file_help.read()
file_help.close()

def ChooseAnimeSite():
    site = 'jutsu'

    url = amine_url_lib[site]

def FindAnime(name: str):

    anime_list = []

    #for jut.su
    if url == amine_url_lib['jutsu']:
        anime_list = jutsu.find_amime(name=name)

    return anime_list

def NoneFunction(message):
    bot.reply_to(message, 'Прости, но пока я не могу отвечать на это, но совсем скоро научусь!')

@bot.message_handler(commands=['start', 'help'])
def command_base(message):
    if message.text == "/start":
        NoneFunction(message)
    if message.text == "/help":
        bot.send_message(message.from_user.id, help_text)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text.lower().split()[0] == 'найди':
        list_anime = FindAnime(' '.join(message.text.lower().split()[1:]))
        reply = "Вот что я нашел на " + url[8:] + ":\n"
        for var in list_anime:
            reply += var + '\n'
        bot.send_message(message.from_user.id, reply)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)