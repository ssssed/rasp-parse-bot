import json
import requests
from bs4 import BeautifulSoup
import os
link = "https://rasp.sstu.ru/"
FILE_NAME = "text.xlsx"
headers = {}


def parse(link):
    r = requests.get(link, headers=headers)
    s = BeautifulSoup(r.text, "html.parser")
    result_list = {}
    groups = s.find_all(class_='col-auto group')
    for group in groups:
        name = group.text
        full_link = link[:-1] + group.find('a').get('href')
        result_list[name] = full_link

    if not os.path.exists('groups'):
        os.mkdir('groups')

    with open('groups/shedule.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    print('File was created')


parse(link)
