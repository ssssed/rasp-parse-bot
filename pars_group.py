import json
import requests
from bs4 import BeautifulSoup
import os
import asyncio
import aiohttp


async def get_page_data(session, url, name):
    headers = {}
    async with session.get(url=url, headers=headers, ssl=False) as response:
        response_text = await response.text()
        time_lesson = ['8:00-9:30', '9:45-11:15',
                       '11:30-13:00', '13:40-15:10', '15:20-16:50', '17:00 - 18:30', '18:40 - 20:10', '20:20 - 21:50']
        soup = BeautifulSoup(response_text, 'lxml')
        days = soup.find_all(lambda tag: tag.name == 'div' and
                                         tag.get('class') == ['day'] or tag.get('class') == ['day', 'day-current'])
        week_rasp = {}
        for day in days:
            day_header = day.find(class_='day-header')
            week = day.find('span').text
            day_name = day_header.text.replace(week, '')
            lessons = day.find_all(class_='day-lesson')
            day_rasp = []
            i = 0
            for lesson in lessons:
                if (lesson.get('class') == ['day-lesson', 'day-lesson-empty']):
                    day_rasp.append({
                        'room': '',
                        'name': '-',
                        'type': '',
                        'teacher': ''

                    })
                    i += 1
                    continue
                lesson_room = lesson.find(class_='lesson-room').text.strip()
                lesson_name = lesson.find(class_='lesson-name').text.strip()
                lesson_type = lesson.find(class_='lesson-type').text.strip()
                lesson_teacher = lesson.find(
                    class_='lesson-teacher').text.strip() or 'Не Указан'
                day_rasp.append({
                    'room': lesson_room,
                    'name': lesson_name,
                    'type': lesson_type,
                    'time': time_lesson[i],
                    'teacher': lesson_teacher
                })
                i += 1
            if (not len(day_rasp)):
                day_rasp = [{'message': 'Нет пар'}]
            week_rasp[day_name] = {
                'day': day_name,
                'week': week,
                'lessons': day_rasp
            }
        with open(f'groups/schedules_group/{name}.json', 'w', encoding='utf-8') as file:
            json.dump(week_rasp, file, indent=4, ensure_ascii=False)
        print(f'Группа {name} была спаршена')
        return week_rasp


async def gather_data():
    async with aiohttp.ClientSession() as session:
        with open('groups/schedule.json', 'r') as file:
            pages = json.load(file)
        tasks = []
        for group_name in pages:
            page = pages[group_name]
            task = asyncio.create_task(get_page_data(session, page, group_name))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())


if __name__ == '__main__':
    main()


class Schedule_Data:

    def _createScheduleGroupsJson(self):
        link = 'https://rasp.sstu.ru/'
        headers = {}
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        result_list = {}
        groups = soup.find_all(class_='col-auto group')
        for group in groups:
            name = group.text
            full_link = link[:-1] + group.find('a').get('href')
            result_list[name] = full_link

        if not os.path.exists('groups'):
            os.mkdir('groups')
            os.mkdir('groups/schedules_group')

        with open('groups/schedule.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)

        print('File was created')
        return result_list

    def getScheduleGroups(self):
        if not os.path.exists('groups'):
            os.mkdir('groups')
            return self._createScheduleGroupsJson()
        else:
            with open('groups/schedule.json', 'r') as file:
                data = json.load(file)
                return data
