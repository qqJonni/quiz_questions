import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv, find_dotenv
import keyboards as kb

load_dotenv(find_dotenv())
bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_hello(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я бот для викторин!', reply_markup=kb.question_button_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
