from asyncore import dispatcher
from email import message
from tokenize import group
from aiogram import Bot, Dispatcher, executor, types
import aiogram
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as style
import json
from app import ParseRasp
TOKEN = '5762024494:AAFgt8CdK9a96VNxqfwTQESDcC34kux3BNA'

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
        if lesson.get('lesson') == '-':
            message += '------------\n' + 'Отдых' + '\n\n'
        else:
            message += style.hbold(lesson.get('lesson')) + \
                '\n' + lesson.get('time') + '\n\n'
    return message


@dp.message_handler(state=[])
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("info", "Информация о боте"),
        types.BotCommand("rasp", "Получить расписание"),
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

    answer = sheduleFormat(app.generateJSON())
    await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
