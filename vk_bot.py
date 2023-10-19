import os
import random
from dotenv import load_dotenv, find_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardColor, VkKeyboard
from quiz_questions import Quiz


class Bot():

    def __init__(self):
        self.quiz = Quiz()
        self.session = None
        load_dotenv(find_dotenv())
        self.session = vk_api.VkApi(token=os.environ.get('VK_TOKEN'))
        self.user_question = None
        self.correct_answer = None
        self.run()

    def send_message(self, user_id, message, keyboard=None):
        post = {
            'user_id': user_id,
            'message': message,
            'random_id': random.randint(1, 20000)  # Increased upper limit to reduce collision possibility
        }

        if keyboard is not None:
            post['keyboard'] = keyboard.get_keyboard()

        self.session.method('messages.send', post)

    def handle_new_question(self, user_id):
        self.user_question, self.correct_answer = self.quiz.get_random_question()
        self.send_message(user_id, self.user_question)

    def run(self):
        for event in VkLongPoll(self.session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                user_id = event.user_id

                if text == 'start':
                    keyboard = VkKeyboard()
                    buttons = ['Новый вопрос', 'Сдаться', 'Мой счет']
                    buttons_color = [VkKeyboardColor.POSITIVE, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE]

                    for button, button_color in zip(buttons, buttons_color):
                        keyboard.add_button(button, button_color)

                    self.send_message(user_id, "Привет! Я бот для викторин! Чтобы начать, нажмите кнопку 'Новый вопрос'.", keyboard)

                elif text == 'новый вопрос':
                    self.handle_new_question(user_id)

                elif text == 'сдаться':
                    self.send_message(user_id, self.correct_answer)

                elif text == 'мой счет':
                    self.send_message(user_id, "Твой счет: 0")  # Just an example, you should track and update the score

                else:
                    if text == self.correct_answer.lower():
                        self.send_message(user_id, "Ты ответил верно!")
                    else:
                        self.send_message(user_id, "Ты ответил неверно.")


if __name__ == "__main__":
    Bot()