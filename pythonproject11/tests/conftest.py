import os

import pytest

from pythonproject11.src.api_connect import ApiVacancies, VacanciesHh  # Импортируем классы
from pythonproject11.src.open_files import JsonHandler


class ConcreteApiVacancies(ApiVacancies):
    """Фикстура для ApiVacancies (абстрактный класс)."""

    def load_vacancies(self, keyword):
        pass


@pytest.fixture
def concrete_api_vacancies():
    """Фикстура для теста test_api_key_getter_setter and test_is_connected_default_false."""
    return ConcreteApiVacancies()


@pytest.fixture
def hh_api():
    """Фикстура для тестов с VacanciesHh классом."""
    return VacanciesHh()


@pytest.fixture
def mock_response(mocker):  # Передаем фикстуру mocker
    """Фикстура для создания мок-ответа в mock_requests_get."""
    mock = mocker.Mock()  # Используем mocker.Mock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {"items": []}  # Default пустой ответ
    return mock


@pytest.fixture
def mock_requests_get(mocker, mock_response):  # Передаем фикстуру mocker
    """Фикстура для мокирования requests.get."""
    # mocker.patch автоматически запускает и останавливает мок
    return mocker.patch("pythonproject11.src.api_connect.requests.get", return_value=mock_response)


@pytest.fixture(scope="function")
def json_handler():
    """Фикстура для предоставления экземпляра JsonHandler с временным файлом."""
    filename = "test_vacancies.json"
    # Убедиться, что файл не существует перед началом теста
    if os.path.exists(filename):
        os.remove(filename)

    handler = JsonHandler(filename)
    yield handler
    # Очистить тестовый файл после выполнения теста
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture(scope="function")
def sample_vacancies():
    """Фикстура для предоставления примеров данных вакансий."""
    return [
        {"url": "https://example.com/python-developer", "title": "Python Developer", "company": "Google"},
        {"url": "https://example.com/data-scientist", "title": "Data Scientist", "company": "Microsoft"},
        {"url": "https://example.com/java-developer", "title": "Java Developer", "company": "Amazon"},
    ]


@pytest.fixture(scope="function")
def sample_vacancies_with_duplicates():
    """Фикстура для предоставления примеров данных вакансий с дубликатами."""
    return [
        {"url": "https://example.com/python-developer", "title": "Python Developer", "company": "Google"},
        {"url": "https://example.com/data-scientist", "title": "Data Scientist", "company": "Microsoft"},
        {
            "url": "https://example.com/python-developer",
            "title": "Python Developer",
            "company": "Google",
        },  # Дублирующийся URL
        {"url": "https://example.com/java-developer", "title": "Java Developer", "company": "Amazon"},
        {
            "url": "https://example.com/data-scientist",
            "title": "Data Scientist",
            "company": "Microsoft",
        },  # Дублирующийся URL
    ]


@pytest.fixture(scope="function")
def sample_vacancies_without_url():
    """Фикстура для предоставления примеров данных вакансий, некоторые из которых без поля 'url'."""
    return [
        {"url": "https://example.com/full-data", "title": "Full Role", "company": "Company A"},
        {"title": "Role without URL 1", "company": "Company B"},  # Отсутствует URL
        {"url": "https://example.com/another-full", "title": "Another Role", "company": "Company C"},
        {"title": "Role without URL 2", "company": "Company D"},  # Отсутствует URL
    ]


@pytest.fixture(scope="function")
def criteria_to_remove_one():
    """Фикстура для функции критериев удаления, нацеленной на одну конкретную вакансию."""

    def _criteria(vacancy):
        return vacancy.get("url") == "https://example.com/python-developer"

    return _criteria


@pytest.fixture(scope="function")
def criteria_to_remove_multiple():
    """Фикстура для функции критериев удаления, нацеленной на несколько вакансий."""

    def _criteria(vacancy):
        return vacancy.get("company") == "Microsoft"

    return _criteria


@pytest.fixture(scope="function")
def criteria_no_match():
    """Фикстура для функции критериев удаления, которая ничего не находит."""

    def _criteria(vacancy):
        return vacancy.get("title") == "NonExistent Role"

    return _criteria


@pytest.fixture(scope="function")
def criteria_raises_error():
    """Фикстура для функции критериев удаления, которая генерирует исключение."""

    def _criteria(vacancy):
        if vacancy.get("company") == "Microsoft":
            raise ValueError("Criteria function encountered an error!")
        return False  # Не должно быть достигнуто, если исключение было сгенерировано

    return _criteria


class DummyVacancy:
    """Простой класс, подобный Vacancy, для тестирования."""

    def __init__(self, title, url, salary_from, salary_to, description):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description


@pytest.fixture(scope="function")
def simple_class():
    """Фикстура простого класса для тестирования Vacancy."""
    return DummyVacancy


@pytest.fixture
def mock_modules(mocker):
    """Фикстура для мокирования внешних зависимостей функции main."""
    # Патчим символы в модуле main (там, где они реально используются)
    mock_vacancies_hh = mocker.patch("pythonproject11.src.main.VacanciesHh")
    mock_json_handler = mocker.patch("pythonproject11.src.main.JsonHandler")
    mock_create_vacancy_objects = mocker.patch("pythonproject11.src.main.create_vacancy_objects")

    mock_hh_instance = mock_vacancies_hh.return_value
    mock_json_handler_instance = mock_json_handler.return_value

    return {
        "input": mocker.patch("builtins.input"),
        # НЕ мокируем print, чтобы capfd корректно считывал вывод
        "hh_api_instance": mock_hh_instance,
        "json_handler_instance": mock_json_handler_instance,
        "create_vacancy_objects": mock_create_vacancy_objects,
    }
