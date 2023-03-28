from os import environ as env

# Забирает токен из окружения
API_TOKEN_BOT = env.get('BOT_TOKEN')

# Забирает текст из файла для команды -> /start
file_start = open('Files/start.txt', 'r', encoding="utf-8")
START_TXT = file_start.read()
file_start.close()

# Забирает текст из файла для команды -> /help
file_help = open('Files/help.txt', 'r', encoding="utf-8")
HELP_TXT = file_help.read()
file_help.close()