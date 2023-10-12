from random import randint


def get_random_question():
    with open('1vs1200.txt', 'r', encoding="KOI8-R") as file:
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
