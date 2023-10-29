from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from quiz_questions import random_question
import os
from dotenv import load_dotenv, find_dotenv


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)


    async def start(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        button_new_question = types.KeyboardButton('Новый вопрос')
        button_give_up = types.KeyboardButton('Сдаться')
        button_my_score = types.KeyboardButton('Мой счет')
        keyboard.add(button_new_question, button_give_up, button_my_score)
        await message.answer("Привет! Я бот для викторин! Чтобы начать, нажмите кнопку 'Новый вопрос'.",
                            reply_markup=keyboard)


    async def send_new_question(message: types.Message):
        question, answer = random_question()
        await dp.storage.set_data(chat=message.chat.id, data={"answer": answer})
        await bot.send_message(chat_id=message.chat.id, text=question)


    async def give_up(message: types.Message):
        data = await dp.storage.get_data(chat=message.chat.id)
        answer = data.get("answer")
        await message.reply(f"Правильный ответ: {answer}")


    async def check_answer(message: types.Message):
        data = await dp.storage.get_data(chat=message.chat.id)
        answer = data.get("answer")
        if answer and message.text.lower() in answer.lower():
            await message.reply("Поздравляю! Это верный ответ!")
        else:
            await message.reply("Это не верный ответ.")

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(send_new_question, lambda message: message.text == 'Новый вопрос')
    dp.register_message_handler(give_up, lambda message: message.text == 'Сдаться')
    dp.register_message_handler(check_answer)

    # Start the bot
    executor.start_polling(dp, skip_updates=True)
