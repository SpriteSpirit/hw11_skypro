from random import shuffle
import requests


class Question:
    def __init__(self, text: str, difficulty: int, correct_answer: str):
        self._text = text
        self.difficulty = int(difficulty)
        self.correct_answer = correct_answer
        self._points = self.points
        self.user_response = None

    @property
    def points(self) -> int:
        """Возвращает количество баллов в зависимости от сложности: 1-10 б, за 5-50 б"""

        return self.difficulty * 10

    @property
    def text(self) -> str:
        """Возвращает вопрос пользователю в шаблонном виде"""

        return f"Вопрос: {self._text}\nСложность {self.difficulty}/5"

    def is_correct(self) -> bool:
        """Возвращает True, если ответ пользователя совпадает с верным ответом, иначе False."""

        return self.user_response == self.correct_answer

    def get_feedback(self) -> str:
        """Возвращает результат проверки ответа"""

        return f"Ответ верный, получено {self.points} баллов" if self.is_correct() \
            else f"Ответ неверный, верный ответ {self.correct_answer}"


def get_data_and_create_quiz(json_link: str) -> list:
    """По ссылке получает список всех вопросов - они считываются и раскладываются в экземпляры класса Question.
    Которые в свою очередь, складываются в список"""

    response = requests.get(json_link)
    questions_json = response.json()

    list_questions = []

    for data in questions_json:
        list_questions.append(Question(data['q'], data['d'], data['a']))

    return list_questions


def do_quiz(list_questions: list) -> tuple[int, int]:
    """Функционал викторины: баллы, перемешанные вопросы по порядку, ответ пользователя, проверка"""

    total_points = 0
    result = []

    shuffle(questions)

    for question in list_questions:
        print(question.text)
        user_answer = input("Ответ: ")
        question.user_response = user_answer

        if question.is_correct():
            print(question.get_feedback())
            total_points += question.points
            result.append(True)
            input("\nНажмите Enter, чтобы продолжить\n")
        else:
            print(question.get_feedback())
            input("\nНажмите Enter, чтобы продолжить\n")

    return total_points, len(result)


def get_results(all_points: int, all_questions: int, answers: int) -> None:
    """Завершаем викторину и подводим итог"""

    print("Вот и всё!")
    print(f"Отвечено верно на {answers} вопросов из {all_questions}")
    print(f"Набрано {all_points} баллов\n")


# запуск викторины с передачей ссылки на json-вопросы и итоги
questions = get_data_and_create_quiz("https://www.jsonkeeper.com/b/ZGUO")
points, results = do_quiz(questions)
get_results(points, len(questions), results)

input("Press any key to exit...")
quit()