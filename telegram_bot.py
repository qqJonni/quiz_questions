import os
import telebot
from telebot import types
from dotenv import load_dotenv, find_dotenv
from quiz_questions import random_question

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    question = types.InlineKeyboardButton('Новый вопрос', callback_data='new_question')
    give_up = types.InlineKeyboardButton('Сдаться', callback_data='give_up')
    my_account = types.InlineKeyboardButton('Мой счёт', callback_data='my_account')
    markup.add(question, give_up, my_account)

    bot.send_message(message.chat.id, 'Привет! Я бот для викторин!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def new_question(call):
    if call.message:
        if call.data == 'new_question':
            bot.send_message(call.message.chat.id, random_question())


if __name__ == '__main__':
    bot.polling()
