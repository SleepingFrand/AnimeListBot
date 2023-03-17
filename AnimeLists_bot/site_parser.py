import requests
from bs4 import BeautifulStoneSoup as BS

class jutsu(object):
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

    @classmethod
    def find_amime(cls, name: str) -> list[str]:
        anime_list = []

        cls.data['show_search'] = name

        jut_su = requests.post('https://jut.su/anime/', cookies=cls.cookies, headers=cls.headers, data=cls.data)
        jut_su_soup = BS(jut_su.content, features='lxml')
        
        for var1 in jut_su_soup.select('div.aaname'):
            anime_list.append(var1.text)

        return anime_list
    





