from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from quiz_questions import random_question
import os
from dotenv import load_dotenv, find_dotenv


class QuizBot:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.dp.register_message_handler(self.start, commands=['start'])
        self.dp.register_message_handler(self.send_new_question, lambda message: message.text == 'Новый вопрос')
        self.dp.register_message_handler(self.give_up, lambda message: message.text == 'Сдаться')
        self.dp.register_message_handler(self.check_answer)
        self.executor = executor


    async def start(self, message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        button_new_question = types.KeyboardButton('Новый вопрос')
        button_give_up = types.KeyboardButton('Сдаться')
        button_my_score = types.KeyboardButton('Мой счет')
        keyboard.add(button_new_question, button_give_up, button_my_score)
        await message.answer("Привет! Я бот для викторин! Чтобы начать, нажмите кнопку 'Новый вопрос'.",
                            reply_markup=keyboard)

    async def send_new_question(self, message: types.Message):
        question, answer = random_question()
        await self.storage.set_data(chat=message.chat.id, data={"answer": answer})
        await self.bot.send_message(chat_id=message.chat.id, text=question)

    async def give_up(self, message: types.Message):
        data = await self.storage.get_data(chat=message.chat.id)
        answer = data.get("answer")
        await message.reply(f"Правильный ответ: {answer}")

    async def check_answer(self, message: types.Message):
        data = await self.storage.get_data(chat=message.chat.id)
        answer = data.get("answer")
        if answer and message.text.lower() in answer.lower():
            await message.reply("Поздравляю! Это верный ответ!")
        else:
            await message.reply("Это не верный ответ.")

    def run(self):
        self.executor.start_polling(self.dp, skip_updates=True)


if __name__ == '__main__':
    quiz_bot = QuizBot()
    quiz_bot.run()
