import os
from dotenv import load_dotenv, find_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardColor, VkKeyboard
from quiz_questions import random_question


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': 0
    }

    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()

    session.method('messages.send', post)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    session = vk_api.VkApi(token=os.environ.get('VK_TOKEN'))

    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            user_id = event.user_id

            if text == 'start':
                keyboard = VkKeyboard()
                buttons = ['Новый вопрос', 'Сдаться', 'Мой счет']
                buttons_color = [VkKeyboardColor.POSITIVE, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE]

                for button, button_color in zip(buttons, buttons_color):
                    keyboard.add_button(button, button_color)

                send_message(user_id, "Привет! Я бот для викторин! Чтобы начать, нажмите кнопку 'Новый вопрос'.",
                             keyboard)

            elif text == 'новый вопрос':
                question, answer = random_question()
                print(question)
                print(answer)
                send_message(user_id, question)
                user_question = question
                correct_answer = answer

            elif text == 'сдаться':
                send_message(user_id, correct_answer)

            elif text == 'мой счет':
                send_message(user_id, "Твой счет:")

            else:
                if text == correct_answer.lower():
                    send_message(user_id, "Ты ответил верно!")
                else:
                    send_message(user_id, "Ты ответил неверно.")
