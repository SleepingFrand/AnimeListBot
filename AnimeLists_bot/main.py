from handlers import handlers, bot, last_interaction_time, time
from utils import SaveUserData
import threading

# Просматривает пользователей и переносит в память тех, кто долго не пишет
def time_cheak():
    while 1:
        for i, t in last_interaction_time.items():
            if time.time() - t >= 300:
                SaveUserData(i)
                del last_interaction_time[i]
        time.sleep(10)


if __name__ == '__main__':
    bot.message_handler = handlers
    
    t1 = threading.Thread(target=time_cheak)

    t1.start()

    bot.infinity_polling()






