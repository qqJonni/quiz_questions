
import argparse
from random import randint


def get_random_question(filename='1vs1200.txt'):
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

    quiz_questions = dict(zip(questions, answers))
    new_quiz_questions = list(quiz_questions.items())

    question, answer = new_quiz_questions[randint(0, len(new_quiz_questions) - 1)]
    questions_list = question, answer

    return questions_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='1vs1200.txt', help='Введите название файла')
    args = parser.parse_args()
    get_random_question(args.filename)
