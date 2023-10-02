from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

question_button = KeyboardButton('Новый вопрос')
give_up = KeyboardButton('Сдаться')
my_account = KeyboardButton('Мой счёт')
question_button_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(question_button, give_up,
                                                                                           my_account)
