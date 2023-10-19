import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from quiz_questions import Quiz


class QuizBot:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.quiz = Quiz()

        self.register_handlers()

    def register_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            button_new_question = types.KeyboardButton('Новый вопрос')
            button_give_up = types.KeyboardButton('Сдаться')
            button_my_score = types.KeyboardButton('Мой счет')
            keyboard.add(button_new_question, button_give_up, button_my_score)
            await message.answer("Привет! Я бот для викторин! Чтобы начать, нажмите кнопку 'Новый вопрос'.", reply_markup=keyboard)

        @self.dp.message_handler(lambda message: message.text == 'Новый вопрос')
        async def send_new_question(message: types.Message):
            question, answer = self.quiz.get_random_question()
            await self.dp.storage.set_data(chat=message.chat.id, data={"answer": answer})
            await self.bot.send_message(chat_id=message.chat.id, text=question)

        @self.dp.message_handler(lambda message: message.text == 'Сдаться')
        async def give_up(message: types.Message):
            data = await self.dp.storage.get_data(chat=message.chat.id)
            answer = data.get("answer")
            await message.reply(f"Правильный ответ: {answer}")

        @self.dp.message_handler()
        async def check_answer(message: types.Message):
            data = await self.dp.storage.get_data(chat=message.chat.id)
            answer = data.get("answer")
            if answer and message.text.lower() in answer.lower():
                await message.reply("Поздравляю! Это верный ответ!")
            else:
                await message.reply("Это не верный ответ.")

    def run(self):
        executor.start_polling(self.dp, skip_updates=True)


if __name__ == '__main__':
    bot = QuizBot()
    bot.run()
