from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as style
import json
import os
from models import models
from dotenv import load_dotenv

today_button = KeyboardButton('На сегодня')
week_button = KeyboardButton('На неделю')
all_button = KeyboardButton('На две недели')
change_group_buttton = KeyboardButton('Сменить группу')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(today_button, week_button, all_button, change_group_buttton)


def dotenv_insert():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


dotenv_insert()

TOKEN = os.environ.get('TOKEN') or ''

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def get_user(chat_id, group_name=''):
    try:
        user = models.User.get(models.User.chat_id == chat_id)
    except:
        user = models.User.create(chat_id=chat_id, group_name=group_name)
    return user


def get_user_group(chat_id):
    try:
        user = models.User.get(models.User.chat_id == chat_id)
        return user.group_name
    except:
        return 'err'


def schedule_format(schedule='null'):
    counter = 0
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
            else:
                counter += 1
    if counter == len(schedule.get('lessons')):
        message += style.hbold('Поздравляю, у тебя нет пар!')
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
    hav_group = get_user_group(chat_id=message.chat.id)
    if (hav_group == 'err'):
        await message.answer('Напишите вашу группу, чтобы получить расписание в формате б1-ПИНФ-22 Например',
                             reply_markup=greet_kb)
    else:
        await message.answer(f'С возвращением, {message.chat.first_name}. Рад вас снова видеть', reply_markup=greet_kb)


@dp.message_handler(commands='info')
async def start(message: types.Message):
    await message.answer(
        'Я бот, созданный Седом. Мой исходный код можно посмотреть тут - https://github.com/ssssed/rasp-parse-bot')


@dp.message_handler(commands='rasp')
async def get_rasp(message: types.Message):
    await message.reply(
        text='Пришлите название вашей группы, например б1-ПИНФ-22', reply=False)


@dp.message_handler(Text(equals='На сегодня'))
async def send_today_schedule(message: types.Message):
    today = str(datetime.now()).split(' ')[0]
    today = today.split('-')
    date = today[-1] + '.' + today[-2]
    group = get_user_group(chat_id=message.chat.id)
    try:
        with open(f'groups/schedules_group/{group}.json') as file:
            schedule = json.load(file)
        answer = schedule_format(schedule[date])
        return await message.answer(answer, reply_markup=greet_kb)
    except:
        return await message.answer(schedule_format())


@dp.message_handler(Text(equals='На неделю'))
async def send_today_schedule(message: types.Message):
    group = get_user_group(chat_id=message.chat.id)
    counter = 0
    try:
        with open(f'groups/schedules_group/{group}.json') as file:
            schedules = json.load(file)
        for day in schedules:
            if schedules[day].get('week') == 'Понедельник':
                counter += 1
            if counter == 2:
                return
            await message.answer(schedule_format(schedules[day]), reply_markup=greet_kb)
        return
    except:
        return await message.answer(schedule_format())


@dp.message_handler(Text(equals='На две неделю'))
async def send_today_schedule(message: types.Message):
    group = get_user_group(chat_id=message.chat.id)
    try:
        with open(f'groups/schedules_group/{group}.json') as file:
            schedule = json.load(file)
        for day in schedule:
            await message.answer(schedule_format(schedule[day]), reply_markup=greet_kb)
        return
    except:
        return await message.answer(schedule_format())


@dp.message_handler(Text(equals='Сменить группу'))
async def send_today_schedule(message: types.Message):
    await message.answer("Введить название вашей группы")


@dp.message_handler(Text)
async def set_group(message: types.Message):
    try:
        with open(f'groups/schedule.json', 'r') as file:
            group_base = json.load(file)
    except Exception as error:
        print('[ Error ]', error)
        await message.answer('Я вас не понимаю', reply_markup=greet_kb)
    if group_base.get(message.text) is not None:
        user = get_user(chat_id=message.chat.id, group_name=message.text)
        user.group_name = message.text
        user.save()
        print('[ USER UPDATE ]')
        await message.answer('Группа успешно обновленна', reply_markup=greet_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
