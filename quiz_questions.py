import argparse
from random import randint


class Quiz:
    def __init__(self, filename='1vs1200.txt'):
        with open(filename, 'r', encoding="KOI8-R") as file:
            content = file.read()
        text = content.split('\n\n')
        questions = []
        answers = []

        for line in text:
            line.strip()
            if line.startswith('Вопрос') or line.startswith('\nВопрос'):
                questions.append(line)
            elif line.startswith('Ответ'):
                answers.append(line)

        self.questions = dict(zip(questions, answers))

    def get_random_question(self):
        new_quiz_questions = list(self.questions.items())
        question, answer = new_quiz_questions[randint(0, len(new_quiz_questions) - 1)]
        return question, answer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='1vs1200.txt', help='Введите название файла')
    args = parser.parse_args()
    quiz = Quiz(args.filename)
    print(quiz.get_random_question())