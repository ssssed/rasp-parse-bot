import requests
from bs4 import BeautifulSoup
import datetime


class ParseRasp(object):
    link = "https://rasp.sstu.ru/rasp/group/22"
    FILE_NAME = "text.xlsx"
    headers = {}
    rasp = []
    today = ''
    timeLesson = ['8:00-9:30', '9:45-11:15',
                  '11:30-13:00', '13:40-15:10', '15:20-16:50']

    def parse(self, link):
        r = requests.get(link, headers=self.headers)
        result_list = {}
        s = BeautifulSoup(r.text, "html.parser")
        days = s.find_all(lambda tag: tag.name == 'div' and
                          tag.get('class') == ['day'] or tag.get('class') == ['day', 'day-current'])
        for day in days:
            day_name = day.find("div", class_="day-header").text[-5:]
            result_list[day_name] = []
            day__lesson = day.find_all("div", class_="lesson-name")
            for i in range(5):
                if (i < len(day__lesson)):
                    result_list[day_name].append(day__lesson[i].text)
                else:
                    result_list[day_name].append("-")
        return result_list

    def nextDay():
        secondDay = datetime.date.today() + datetime.timedelta(days=1)
        return secondDay

    def getToday(self):
        today = datetime.date.today()
        today = str(today).split('-')[1:]
        today = today[1] + '.' + today[0]
        return today

    def generateJSON(self):
        today = self.getToday()
        lessons = self.parse(self.link)
        i = 0
        for lesson in lessons[today]:
            self.rasp.append(
                {'id': i + 1, "time": self.timeLesson[i], "lesson": lesson})
            i += 1
        return self.rasp


parsLesson = ParseRasp()
print(parsLesson.generateJSON())
