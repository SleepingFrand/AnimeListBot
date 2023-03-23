from handlers import handlers, bot

if __name__ == '__main__':
    bot.message_handler = handlers
    bot.infinity_polling()




