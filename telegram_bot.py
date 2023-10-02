import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv, find_dotenv
from aiogram.types import ReplyKeyboardMarkup

load_dotenv(find_dotenv())
bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)
question_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row('Новый вопрос', 'Сдаться',
                                                                                           'Мой счёт')


@dp.message_handler(commands=['start'])
async def process_hello(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я бот для викторин!', reply_markup=question_button)


@dp.message_handler(text='Новый вопрос')
async def new_question(message: types.Message):
    await message.answer('Вопрос: О чем профессор Генри Бичер сказал, что этому "можно дать'
                                                 ' научное и теологическое определение, но невозможно дать юридическое"?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
