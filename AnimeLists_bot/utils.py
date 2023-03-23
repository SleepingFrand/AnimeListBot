import json

class Anime:
    def __init__(self, title : str, genre : str, description : str, episodes : int, watched : int, site : str):
        self.title = title
        self.genre = genre
        self.description = description
        self.episodes = episodes
        self.watched = watched
        self.site = site

    # ����������� ������� Anime � JSON
    def to_json(self):
        return json.dumps({
            "title": self.title,
            "genre": self.genre,
            "description": self.description,
            "episodes": self.episodes,
            "watched": self.watched,
            "site": self.site
        })

    # �������� ������� Anime �� JSON
    @classmethod
    def from_json(cls, json_str : str):
        json_dict = json.loads(json_str)
        return cls(title=json_dict['title'], genre=json_dict['genre'], description=json_dict['description'], episodes=json_dict['episodes'], watched=json_dict['watched'], site=json_dict['site'])

class database(object):
    # ������� ���������� ������ ������������
    @classmethod
    def save_user_data(cls, user_chat_id : str, anime_info : str):
        with open(f'data/{user_chat_id}.json', 'w') as f:
            f.write(anime_info)
    
    # ������� ������ ������ ������������  
    @classmethod 
    def load_user_data(cls, user_chat_id : str):
        try:
            with open(f'data/{user_chat_id}.json', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return {}

def AnimeListToFile(user_chat_id : int, animelist : list(Anime)):
    if not animelist:
        return
    json_str = str()
    for item in animelist:
        json_str += f"|{item.to_json()}"
    database.save_user_data(str(user_chat_id), json_str)

def FileToAnimeList(user_chat_id : int) -> list(Anime):
    json_str = database.load_user_data(str(user_chat_id))
    return [Anime.from_json(item) for item in json_str.split('|') if item]

Anime_data = dict[int:list(Anime)]

def GetListFromData(user_chat_id : int) -> list(Anime):
    global Anime_data

    if user_chat_id not in Anime_data.keys:
        Anime_data[user_chat_id] = FileToAnimeList(user_chat_id)
    return Anime_data[user_chat_id]

def SaveUserData(user_chat_id : int):
    global Anime_data

    if user_chat_id not in Anime_data.keys:
        return
    AnimeListToFile(user_chat_id, Anime_data[user_chat_id])
    del Anime_data[user_chat_id]



