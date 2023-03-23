from ast import Return
import requests
from bs4 import BeautifulSoup  as BS
from bs4 import Tag, NavigableString
from utils import Anime

amine_url_lib = { 
    'jutsu' : 'https://jut.su/anime/'
    }

# Класс для парса jut.su
class jutsu(object):
    # Данные для загрузки сайта
    cookies = {
        '_ym_uid': '167887747395825577',
        '_ym_d': '1678877473',
        'PHPSESSID': 'f3ksaa6vt4efc4bicr29sk1pa7',
    }
    headers = {
        'authority': 'jut.su',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://jut.su',
        'referer': 'https://jut.su/anime/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'ajax_load': 'yes',
        'start_from_page': '1',
        'show_search': '',
        'anime_of_user': '',
    }

    # Поиск Аниме на сайте по имени
    @classmethod
    def find_amime(cls, name: str) -> dict[str:str]:
        anime_list = dict()

        cls.data['show_search'] = name

        jut_su = requests.post('https://jut.su/anime/', cookies=cls.cookies, headers=cls.headers, data=cls.data)
        jut_su_soup = BS(jut_su.content, features='lxml')

        for i, var1 in enumerate(jut_su_soup.select('div > a')):
            anime_list[var1.find('div', class_='aaname').text] = var1["href"]

        return anime_list

    @classmethod
    def info_per_url(cls, short_url: str) -> Anime:
        anime_info = Anime()
        
        jut_su = requests.post('https://jut.su' + short_url, cookies=cls.cookies, headers=cls.headers)
        jut_su_soup = BS(jut_su.text, features='html.parser')

        ### имя ###

        anime_info.title = jut_su_soup.find('meta', attrs={'property': 'yandex_recommendations_title'})['content']

        ### серии ###

        cls.data['show_search'] = anime_info.title.replace('-', ' ').replace(':', '')

        episodes_req = requests.post('https://jut.su/anime/', cookies=cls.cookies, headers=cls.headers, data=cls.data)
        episodes_html = BS(episodes_req.content, features='lxml')

        for var in episodes_html.select('div.aailines'):
            for i, item in enumerate(var.contents):
                if type(item) == NavigableString:
                    if var.contents[i].split()[1][:3] == 'сер':
                        try:
                            anime_info.episodes = int(var.contents[i].split()[0])
                            break
                        except :
                            pass

        ### ссылка ###

        anime_info.site = 'https://jut.su' + short_url

        ### жанры ###
        genre_html = jut_su_soup.select('#dle-content > div > div > div > div')[0]
        
        genre_list = list()

        for item in genre_html.contents:
            if type(item) == Tag:
                if item.name == 'a':
                    genre_list.append(item.contents[1])
                elif item.name == 'br':
                    break
        
        anime_info.genre = genre_list

        ### описание ###

        description_html = jut_su_soup.select_one('#dle-content > div > div > div > p > span')
        for x in description_html.select('i'):
            x.decompose()
        for x in description_html.select('span'):
            x.decompose()
        anime_info.description = description_html.text

        return anime_info
