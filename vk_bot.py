import os
from dotenv import load_dotenv, find_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardColor, VkKeyboard


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': 0
    }

    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post
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

