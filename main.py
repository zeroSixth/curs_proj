from abc import ABC, abstractmethod
import requests
import json
import os


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query):
        pass


class HeadHunterAPI(VacancyAPI):
    def get_vacancies(self, query):
        url = "https://api.hh.ru/vacancies"
        params = {"text": query, "area": "113"}  # area 113 соответствует России
        response = requests.get(url, params=params)
        return response.json()


class Vacancy:
    def __init__(self, title, link, salary, description):
        self.title = title
        self.link = link
        self.description = description if description else ""  # Обеспечиваем, что описание будет строкой
        self.min_salary = 0
        self.salary = "Зарплата не указана"

        if salary:
            if 'from' in salary and salary['from']:
                self.min_salary = salary['from']
                self.salary = f"от {salary['from']}"
            if 'to' in salary and salary['to']:
                self.salary += f" до {salary['to']}"
            if 'currency' in salary and salary['currency']:
                self.salary += f" {salary['currency']}"

    def __lt__(self, other):
        return self.min_salary < other.min_salary

    @staticmethod
    def cast_to_object_list(vacancies_json):
        vacancies = []
        for item in vacancies_json['items']:
            title = item['name']
            link = item['alternate_url']
            salary = item.get('salary', None)  # Получаем данные о зарплате
            description = item.get('snippet', {}).get('requirement', '')
            vacancy = Vacancy(title, link, salary, description)
            vacancies.append(vacancy)
        return vacancies


class JSONSaver:
    def __init__(self, filename='Data/vacancies.json'):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def add_vacancy(self, vacancy):
        try:
            with open(self.filename, 'r') as file:
                vacancies = json.load(file)
        except FileNotFoundError:
            vacancies = []

        vacancies.append(vacancy.__dict__)

        with open(self.filename, 'w') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)


def get_top_vacancies(vacancies_list, n):
    sorted_vacancies = sorted(vacancies_list, key=lambda x: x.min_salary, reverse=True)
    return sorted_vacancies[:n]


def find_vacancies_by_keyword(vacancies_list, keyword):
    return [vac for vac in vacancies_list if vac.description and keyword.lower() in vac.description.lower()]


def user_interaction():
    hh_api = HeadHunterAPI()
    query = input("Введите поисковый запрос: ")
    vacancies_json = hh_api.get_vacancies(query)
    vacancies_list = Vacancy.cast_to_object_list(vacancies_json)

    # Топ N вакансий по зарплате
    n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_vacancies = get_top_vacancies(vacancies_list, n)
    print("\nТоп вакансий по зарплате:")
    for vac in top_vacancies:
        print(f"{vac.title} - {vac.salary}")

    # Вакансии с ключевым словом в описании
    keyword = input("\nВведите ключевое слово для поиска в описании: ")
    keyword_vacancies = find_vacancies_by_keyword(vacancies_list, keyword)
    print("\nВакансии с ключевым словом в описании:")
    for vac in keyword_vacancies:
        print(f"{vac.title} - {vac.description[:100]}...")

    # Запрос на сохранение данных
    save_data = input("\nХотите сохранить результаты запроса? (да/нет): ")
    if save_data.lower() == "да":
        saver = JSONSaver()
        for vacancy in vacancies_list:  # Сохраняем все вакансии полученные по запросу
            saver.add_vacancy(vacancy)
        print("Данные сохранены в файл vacancies.json в директории Data.")


if __name__ == "__main__":
    user_interaction()
