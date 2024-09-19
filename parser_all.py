import requests
from bs4 import BeautifulSoup
import json

url_f = 'http://karty-mira.ru/city-a.htm'

html = requests.get(url=url_f)
soup = BeautifulSoup(html.content, 'html.parser')
urls = soup.find_all('p')[-14]
urls.find('a')
urls = [i.split('"')[0] for i in str(urls).split('href="')[2:]]


def parser(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    cities = soup.find_all('p')[-15].text
    cities = cities.split('\n')
    cities = [i.split(' - ')[0].replace('ё', 'е').replace('Ё', 'Е') for i in cities]
    return cities


all_cities = []
for url in urls:
    all_cities.extend(parser(url))

with open('cities_all.json', 'w') as f:
    json.dump(all_cities, f)


def get_cites_all():
    with open('cities_all.json') as f:
        cities = json.load(f)
    return cities
