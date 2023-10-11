from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv, find_dotenv
from random import randint

load_dotenv(find_dotenv())
bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Новый вопрос'))
keyboard.insert(KeyboardButton('Сдаться'))
keyboard.add(KeyboardButton('Мой счет'))


def random_question():
    with open('1vs1200.txt', 'r', encoding="KOI8-R") as file:
        content = file.read()
    text = content.split('\n\n')

    questions = []
    answers = []

    for i in text:
        i.strip()
        if i.startswith('Вопрос') or i.startswith('\nВопрос'):
            questions.append(i)
        elif i.startswith('Ответ'):
            answers.append(i)

    quiz_dictionary = dict(zip(questions, answers))
    quiz_list = list(quiz_dictionary.items())

    key, value = quiz_list[randint(0, len(quiz_list) - 1)]
    lst = key, value

    return lst


question, answer = random_question()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text='Привет! Я бот для викторин!', reply_markup=keyboard)
    await message.delete()


@dp.message_handler()
async def new_question(message: types.Message):
    if message.text == 'Новый вопрос':
        global question, answer
        question, answer = random_question()
        print(question)
        print(answer)
        await message.answer(text=question)
        await message.delete()


@dp.message_handler()
async def random_answer(message: types.Message):
    if answer in message.text:
        await message.reply('Правильно! Поздравляю! Для следующего вопроса нажми "Новый вопрос".')
    else:
        await message.reply('Неправильно… Попробуешь ещё раз?')


@dp.message_handler()
async def handle_message(message: types.Message):
    await message.answer("Не знаю ответа. Выберите вариант из меню.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
