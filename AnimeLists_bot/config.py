from os import environ as env

API_TOKEN_BOT = env.get('BOT_TOKEN')

# ��������� ���� � ������� -> /help
file_start = open('Files/start.txt', 'r', encoding="utf-8")
START_TXT = file_start.read()
file_start.close()

# ��������� ���� � ������� -> /help
file_help = open('Files/help.txt', 'r', encoding="utf-8")
HELP_TXT = file_help.read()
file_help.close()


