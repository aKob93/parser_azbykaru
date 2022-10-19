import requests
from bs4 import BeautifulSoup
import json

LETTERS = ['A', 'B', 'V', 'G', 'D', 'Je', 'Zh', 'Z', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F',
           'H', 'Sh', 'E', 'Yu', 'Ya']
URL = 'https://azbyka.ru/days/menology/'
data = {
}


def get_all_pages():
    count = 1
    headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'}
    for letter in LETTERS:

        response_letter = requests.get(url=f'{URL}{letter}', headers=headers)
        soup_letter = BeautifulSoup(response_letter.text, features='html.parser')
        sainted = soup_letter.find('table', class_='menology pad-m').find_all('td', class_='menology-name')
        for saint in sainted:
            name_saint = saint.text.strip()
            response_date = requests.get(url=f'{URL[0:17]}{saint.a["href"]}', headers=headers)
            soup_date = BeautifulSoup(response_date.text, features='html.parser')
            memorial_days = soup_date.find('div', class_='brif').find_all('a')
            print(f'#{count} Имя святого - {name_saint}')
            for day in memorial_days:
                date = day.text.strip()
                if data.get(date, False) is False:
                    data[date] = [name_saint]
                else:
                    data[date].append(name_saint)
            count += 1
    print(f'Всего святых - {count}')
    with open('data_file.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=5)


get_all_pages()
