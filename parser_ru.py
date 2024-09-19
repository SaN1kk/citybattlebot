import requests
from bs4 import BeautifulSoup
import json

url_f = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'


def parser_ru(url):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find('table')
    cities_raw = cities_raw.find_all('td')
    cities_raw = [i.text for i in cities_raw]
    cities = []
    for i in range(2, len(cities_raw), 9):
        cities.append(cities_raw[i].replace('не призн.', '').replace('ё', 'е').replace('Ё', 'Е'))
    return cities


ru_cities = parser_ru(url_f)

with open('cities_ru.json', 'w') as f:
    json.dump(ru_cities, f)


def get_cites_ru():
    with open('cities_ru.json') as f:
        cities = json.load(f)
    return cities
