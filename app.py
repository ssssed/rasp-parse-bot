import requests
from bs4 import BeautifulSoup
import datetime


class ParseRasp():
    link = "https://rasp.sstu.ru/rasp/group/22"
    FILE_NAME = "text.xlsx"
    headers = {}
    week = ''
    today = ''
    timeLesson = ['8:00-9:30', '9:45-11:15',
                  '11:30-13:00', '13:40-15:10', '15:20-16:50']

    def parse(self, link):
        r = requests.get(link, headers=self.headers)
        s = BeautifulSoup(r.text, "html.parser")
        days = s.find_all(lambda tag: tag.name == 'div' and
                          tag.get('class') == ['day'] or tag.get('class') == ['day', 'day-current'])
        week_rasp = {}
        for day in days:
            day_header = day.find(class_='day-header')
            week = day.find('span').text
            day_name = day_header.text.replace(week, '')
            lessons = day.find_all(lambda tag: tag.get('class') == ['day-lesson'] and
                                   tag.get('class') != ['day-lesson', 'day-lesson-empty'])
            day_rasp = []
            for lesson in lessons:
                lesson_room = lesson.find(class_='lesson-room').text
                lesson_name = lesson.find(class_='lesson-name').text
                lesson_type = lesson.find(class_='lesson-type').text
                lesson_teacher = lesson.find(
                    class_='lesson-teacher').text or 'Не Указан'
                day_rasp.append({
                    'room': lesson_room,
                    'name': lesson_name,
                    'type': lesson_type,
                    'teacher': lesson_teacher
                })
            if (not len(day_rasp)):
                day_rasp = [{'message': 'Нет пар'}]
            week_rasp[day_name] = {
                'day': day_name,
                'week': week,
                'lessons': day_rasp
            }
        return week_rasp

    def nextDay(self):
        secondDay = datetime.date.today() + datetime.timedelta(days=1)
        return secondDay

    def getToday(self):
        today = datetime.date.today()
        today = str(today).split('-')[1:]
        today = today[1] + '.' + today[0]
        return today

    def getLessons(self, data):
        lessons = []
        i = 0
        for lesson in data:
            lessons.append({'time': self.timeLesson[i], 'lesson': lesson})
            i += 1
        return lessons

    def generateJSON(self):
        today = self.getToday()
        pars = self.parse(self.link)
        lessons = self.getLessons(pars[today])

        return {
            'day': today,
            'week': self.week,
            'lessons': lessons
        }

# app = ParseRasp()
# print(app.parse("https://rasp.sstu.ru/rasp/group/22"))
