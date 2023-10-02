import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv, find_dotenv


def start():
    load_dotenv(find_dotenv())
    bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
    dp = Dispatcher(bot)
    dp.register_message_handler(lambda message: send_echo(message))
    executor.start_polling(dp, skip_updates=True)


async def send_echo(message: types.Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    start()
