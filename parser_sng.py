import requests
from bs4 import BeautifulSoup
import json
from parser_ru import parser_ru

url_arm = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%90%D1%80%D0%BC%D0%B5%D0%BD%D0%B8%D0%B8'
url_by = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%91%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%B8%D0%B8'
url_ru = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'
url_uzb = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%A3%D0%B7%D0%B1%D0%B5%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD%D0%B0'
url_uk = 'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%8B'
url_kz = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD%D0%B0'

urls_for_tables = {
    'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%A2%D1%83%D1%80%D0%BA%D0%BC%D0%B5%D0%BD%D0%B8%D1%81%D1%82%D0%B0%D0%BD%D0%B0': (
        0, 6),
    'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%93%D1%80%D1%83%D0%B7%D0%B8%D0%B8': (1, 12),
    'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%A2%D0%B0%D0%B4%D0%B6%D0%B8%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD%D0%B0': (
        0, 7),
    'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%9C%D0%BE%D0%BB%D0%B4%D0%B0%D0%B2%D0%B8%D0%B8': (
        2, 10),
    'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%9A%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD%D0%B0': (
        0, 7),
    'https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%90%D0%B7%D0%B5%D1%80%D0%B1%D0%B0%D0%B9%D0%B4%D0%B6%D0%B0%D0%BD%D0%B0': (
        1, 7)
}


def parser_tables(url, start, end):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find('table')
    cities_raw = cities_raw.find_all('td')
    cities_raw = [i.text for i in cities_raw]
    cities = []
    for i in range(start, len(cities_raw), end):
        cities.append(cities_raw[i])
    cities = [i.split('[')[0].split(' (')[0].strip('\n').replace('ё', 'е').replace('Ё', 'Е') for i in cities]
    return cities


def parser_kz(url):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find_all('table')[1]
    cities_raw = cities_raw.find_all('td')
    cities_raw = [i.text for i in cities_raw]
    cities = []
    for i in range(0, len(cities_raw), 12):
        cities.append(cities_raw[i])
    cities = [i.split(', ')[0].split('[')[0].split(' (')[0].strip('\n').replace('ё', 'е').replace('Ё', 'Е') for i in
              cities]
    return cities


def parser_arm(url):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find(class_='mw-body-content')
    cities_raw = cities_raw.find_all('b')
    cities = [i.text.replace('ё', 'е').replace('Ё', 'Е') for i in cities_raw if not str(i.text).isdigit()]
    return cities


def parser_by(url):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find_all('table')[1:7]
    cities = []
    for i in cities_raw:
        cities.extend([j.text for j in i.find_all('td')])

    ready_cities = []
    for i in range(1, len(cities), 6):
        ready_cities.append(cities[i].split('(')[0].split('[')[0].strip('\n').replace('ё', 'е').replace('Ё', 'Е'))

    return ready_cities


def parser_uzb(url):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find_all('table')[:14]
    cities = []
    for i in cities_raw:
        cities.extend([j.text for j in i.find_all('td')])

    ready_cities = []
    for i in range(0, len(cities), 6):
        ready_cities.append(cities[i].split('(')[0].split('[')[0].strip('\n').replace('ё', 'е').replace('Ё', 'Е'))

    return ready_cities


def parser_uk(url):
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text, 'lxml')
    cities_raw = soup.find_all('table')[2]
    cities = [j.text for j in cities_raw.find_all('td')]
    ready_cities = []
    for i in range(1, len(cities), 6):
        ready_cities.append(cities[i].split('(')[0].split('[')[0].strip('\n').replace('ё', 'е').replace('Ё', 'Е'))

    return ready_cities


sng_cities = []
for url, (start, end) in urls_for_tables.items():
    sng_cities.extend(parser_tables(url, start, end))

sng_cities.extend(parser_kz(url_kz))
sng_cities.extend(parser_arm(url_arm))
sng_cities.extend(parser_by(url_by))
sng_cities.extend(parser_ru(url_ru))
sng_cities.extend(parser_uzb(url_uzb))
sng_cities.extend(parser_uk(url_uk))

with open('cities_sng.json', 'w') as f:
    json.dump(sng_cities, f)


def get_cites_sng():
    with open('cities_sng.json') as f:
        cities = json.load(f)
    return cities
