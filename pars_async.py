import requests
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp


LETTERS = ['A', 'B', 'V', 'G', 'D', 'Je', 'Zh', 'Z', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F',
           'H', 'Sh', 'E', 'Yu', 'Ya']
URL = 'https://azbyka.ru/days/menology/'
HEADERS = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'}
data_saints = {}


async def get_saint_data(saint, count):
    name_saint = saint.text.strip()

    connector = aiohttp.TCPConnector(limit=60)
    async with aiohttp.ClientSession(connector=connector) as session:
        response = await session.get(url=f'{URL[0:17]}{saint.a["href"]}', headers=HEADERS)
        soup = BeautifulSoup(await response.text(), features='html.parser')
        memorial_days = soup.find('div', class_='brif').find_all('a')
        print(f'#{count} Имя святого - {name_saint}')

        for day in memorial_days:
            date = day.text.strip()
            if data_saints.get(date, False) is False:
                data_saints[date] = [name_saint]
            else:
                data_saints[date].append(name_saint)


async def get_all_pages():
    count = 1

    for letter in LETTERS:
        try:
            response = requests.get(url=f'{URL}{letter}', headers=HEADERS)
            soup = BeautifulSoup(response.text, features='html.parser')
            sainted = soup.find('table', class_='menology pad-m').find_all('td', class_='menology-name')
            tasks = []

            for saint in sainted:
                task = asyncio.create_task(get_saint_data(saint, count))
                tasks.append(task)
                count += 1
                # в windows(64 разрядной) используется максимум 64 сокета в цикле asyncio, поэтому при достижении
                # 60(округлил) задач идёт выполнение
                if len(tasks) % len(sainted) == 0:
                    await asyncio.gather(*tasks)
                elif len(tasks) % 60 == 0:
                    await asyncio.gather(*tasks)

        except Exception:
            print(Exception)

    print(f'Всего святых - {count}')


def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_all_pages())
    with open('data_saints.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_saints, json_file, ensure_ascii=False, indent=5)


if __name__ == '__main__':
    main()
