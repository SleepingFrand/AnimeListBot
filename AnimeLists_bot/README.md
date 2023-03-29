├── main.py
│   ├── main - Запуск бота
│   └── Отслеживание AFK
├── config.py
│   ├── API_TOKEN - API токен бота
│   └── Файлы с текстом start и help
├── handlers.py
│   ├── commands - Определение команд для бота
|   |   # шаблон данных для кнопок: title_command_data1_..._dataN
│   ├── messages - Определение ответов на сообщения
│   └── errors - Обработка ошибок при выполнении команд
├── utils.py
│   └── database - Взаимодействие с базой данных
├── site_parser.py
│   └── хранит функции парса сайтов
└── data
    ├── 12345.json
    │   # Пример содержимого файла:
    │   # {
    │   #     "title": "Attack on Titan",
    │   #     "genre": "Action, Drama, Fantasy, Military, Mystery",
    │   #     "description": "Several hundred years ago, humans were nearly exterminated by titans.",
    │   #     "episodes": 25,
    │   #     "watched": 13,
    │   #     "site": "Crunchyroll"
    │   # }
    ├── 56789.json
    └── ...
