from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as style
import json
from app import ParseRasp
import os
from dotenv import load_dotenv


def dotenv_insert():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


dotenv_insert()

TOKEN = os.environ.get('TOKEN') or ''

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
app = ParseRasp()
shedule_base = {}

with open('groups/shedule.json', 'r') as file:
    shedule_base = json.load(file)


def sheduleFormat(shedule):
    name = style.hbold(f"{shedule.get('week')} | {shedule.get('day')}")
    message = name + '\n\n'
    for lesson in shedule.get('lessons'):
        if lesson.get('message') == 'Нет Пар':
            message += '------------\n' + 'Отдых' + '\n\n'
        else:
            if lesson.get('name') != '-':
                message += style.hbold(lesson.get('name')) + ' ' + lesson.get('type') + '\n' + \
                           'Кабинет: ' + style.hitalic(lesson.get('room'))+'\n' + 'Время: ' + lesson.get('time') + \
                    '\nПреподаватель: ' + style.hitalic(lesson.get('teacher')) + '\n\n'
    return message


@dp.message_handler(state=[])
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("info", "Информация о боте"),
        types.BotCommand("rasp", "Получить расписание на сегодня"),
        types.BotCommand("rasp-next", "Получить расписание на следуюищй день"),
        types.BotCommand("help", "Помощь"),
    ])


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Напишите вашу группу, чтобы получить расписание в формате б1-ПИНФ-22 Например')


@dp.message_handler(commands='info')
async def start(message: types.Message):
    await message.answer('Я бот, созданный Седом. Мой исходный код можно посмотреть тут - https://github.com/ssssed/rasp-parse-bot')


@dp.message_handler(commands='rasp')
async def get_rasp(message: types.Message):
    await message.reply(
        text='Пришлите название вашей группы, например б1-ПИНФ-22', reply=False)


@dp.message_handler(Text)
async def sendShedule(message: types.Message):
    group = str(message.text)
    link = str(shedule_base[group])
    app.link = link
    today = app.getToday()
    answer = sheduleFormat(app.parse(link)[today])
    await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
