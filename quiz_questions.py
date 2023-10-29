from random import randint


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
    quiz_list = list(quiz_dictionary.items())

    key, value = quiz_list[randint(0, len(quiz_list) - 1)]
    lst = key, value

    return lst


if __name__ == '__main__':
    question, answer = random_question()

