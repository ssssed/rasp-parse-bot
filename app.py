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
        result_list = {}
        s = BeautifulSoup(r.text, "html.parser")
        days = s.find_all(lambda tag: tag.name == 'div' and
                          tag.get('class') == ['day'] or tag.get('class') == ['day', 'day-current'])
        max_count_lessons = int(s.find_all(
            'div', class_='day-lesson day-lesson-hour')[-1].find('span').text)
        for day in days:
            day_header = day.find("div", class_="day-header")
            day_name = day_header.text[-5:]
            if (self.getToday() == day_name):
                self.week = day_header.text[:-5]
            result_list[day_name] = []
            day__lesson = day.find_all("div", class_="lesson-name")
            for i in range(max_count_lessons):
                if (i < len(day__lesson)):
                    result_list[day_name].append(day__lesson[i].text)
                else:
                    result_list[day_name].append("-")
        return result_list

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
