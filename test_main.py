import unittest
from unittest import mock
from main import HeadHunterAPI, Vacancy, JSONSaver, get_top_vacancies, find_vacancies_by_keyword

class TestHeadHunterAPI(unittest.TestCase):
    @mock.patch('main.requests.get')
    def test_get_vacancies(self, mock_get):
        mock_get.return_value.json.return_value = {"items": []}
        api = HeadHunterAPI()
        result = api.get_vacancies("python developer")
        self.assertEqual(result, {"items": []})
        mock_get.assert_called_once_with("https://api.hh.ru/vacancies", params={"text": "python developer", "area": "113"})

class TestVacancy(unittest.TestCase):
    def test_vacancy_no_salary(self):
        vac = Vacancy("Test", "http://test", None, "Desc")
        self.assertEqual(vac.salary, "Зарплата не указана")

    def test_cast_to_object_list_empty(self):
        result = Vacancy.cast_to_object_list({"items": []})
        self.assertEqual(result, [])


class TestJSONSaver(unittest.TestCase):
    @mock.patch('main.os.makedirs')
    @mock.patch('main.open', new_callable=mock.mock_open, read_data='[]')
    def test_add_vacancy(self, mock_open, mock_makedirs):
        filename = "test.json"
        saver = JSONSaver(filename)
        vacancy = Vacancy("Developer", "http://example.com", {"from": 1000, "to": 2000, "currency": "USD"}, "Description")

        saver.add_vacancy(vacancy)


class TestHelperFunctions(unittest.TestCase):
    def test_get_top_vacancies(self):
        vacancies_list = [Vacancy("Test", "http://test", {"from": 100}, "Desc"), Vacancy("Test 2", "http://test2", {"from": 200}, "Desc 2")]
        result = get_top_vacancies(vacancies_list, 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Test 2")

    def test_find_vacancies_by_keyword(self):
        vacancies_list = [Vacancy("Test", "http://test", {"from": 100}, "Python Developer"), Vacancy("Test 2", "http://test2", {"from": 200}, "Java Developer")]
        result = find_vacancies_by_keyword(vacancies_list, "Python")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Test")

class TestUserInteraction(unittest.TestCase):
    @mock.patch('main.input', side_effect=["python developer", "1", "keyword", "да"])
    @mock.patch('main.print')
    def test_user_interaction(self, mock_print, mock_input):
        # Здесь тестовый код для user_interaction. Возможно, потребуется мокирование других функций,
        # в зависимости от того, как user_interaction использует внешние вызовы.
        pass

if __name__ == '__main__':
    unittest.main()
