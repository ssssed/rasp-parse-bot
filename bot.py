from asyncore import dispatcher
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

TOKEN = '5762024494:AAFgt8CdK9a96VNxqfwTQESDcC34kux3BNA'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=[])
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("info", "Информация о боте"),
        types.BotCommand("help", "Помощь"),
    ])


@dp.message_handler(commands='start')
async def start(message: types.Message):

    await message.answer('Вас приветствует бот Гнилой Помидор, чтобы узнать, что я умею напишите /help')


@dp.message_handler(commands='info')
async def start(message: types.Message):
    await message.answer('Я бот, созданный Седом. Мой исходный код можно посмотреть тут - https://github.com/ssssed/rasp-parse-bot')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
