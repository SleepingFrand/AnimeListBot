from handlers import handlers, bot

if __name__ == '__main__':
    bot.handlers = handlers
    bot.infinity_polling()




