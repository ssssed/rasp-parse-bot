from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as style
import json
import os
from dotenv import load_dotenv


today_button = KeyboardButton('На сегодня')
week_button = KeyboardButton('На неделю')
all_button = KeyboardButton('На две недели')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(today_button, week_button, all_button)
def dotenv_insert():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


dotenv_insert()

TOKEN = os.environ.get('TOKEN') or ''

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

with open('groups/schedule.json', 'r') as file:
    schedule_base = json.load(file)


def schedule_format(schedule='null'):
    if (schedule == 'null'):
        return style.hbold('На данный день отсутствует какая-либо информация по парам')
    name = style.hbold(f"{schedule.get('week')} | {schedule.get('day')}")
    message = name + '\n\n'
    for lesson in schedule.get('lessons'):
        if lesson.get('message') == 'Нет Пар':
            message += '------------\n' + 'Отдых' + '\n\n'
        else:
            if lesson.get('name') != '-':
                message += style.hbold(lesson.get('name')) + ' ' + lesson.get('type') + '\n' + \
                           'Кабинет: ' + style.hitalic(lesson.get('room')) + '\n' + 'Время: ' + lesson.get('time') + \
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
    await message.answer('Напишите вашу группу, чтобы получить расписание в формате б1-ПИНФ-22 Например', reply_markup=greet_kb)


@dp.message_handler(commands='info')
async def start(message: types.Message):
    await message.answer(
        'Я бот, созданный Седом. Мой исходный код можно посмотреть тут - https://github.com/ssssed/rasp-parse-bot')


@dp.message_handler(commands='rasp')
async def get_rasp(message: types.Message):
    await message.reply(
        text='Пришлите название вашей группы, например б1-ПИНФ-22', reply=False)


@dp.message_handler(Text)
async def send_schedule(message: types.Message):
    today = str(datetime.now()).split(' ')[0]
    today = today.split('-')
    date = today[-1] + '.' + today[-2]
    group = str(message.text)
    try:
        with open(f'groups/schedules_group/{group}.json') as file:
            schedule = json.load(file)
        answer = schedule_format(schedule[date])
        return await message.answer(answer, reply_markup=greet_kb)
    except Exception as error:
        return await message.answer(schedule_format())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
