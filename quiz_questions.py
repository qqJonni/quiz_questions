from random import choice


def random_question():
    with open('1vs1200.txt', 'r', encoding="KOI8-R") as file:
        content = file.read()
    text = content.split('\n\n')

    questions = []
    answers = []

    for i in text:
        i.strip()
        if i.startswith('Вопрос') or i.startswith('\nВопрос'):
            questions.append(i)
        elif i.startswith('Ответ'):
            answers.append(i)

    quiz_dictionary = dict(zip(questions, answers))
    random_question = choice(list(quiz_dictionary.keys()))

    return random_question
