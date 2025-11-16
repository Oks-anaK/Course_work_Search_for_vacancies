import pytest
import requests


# Тесты для VacanciesHh (конкретный класс)
def test_connect_api_success(hh_api, mock_requests_get):
    """Успешное подключение к API."""
    # mock_requests_get - это замокированный requests.get из фикстуры
    hh_api._connect_api()
    assert hh_api.is_connected is True
    # Проверяем, что requests.get был вызван
    mock_requests_get.assert_called_once()


def test_connect_api_failure(hh_api, mock_requests_get):
    """Неудачное подключение к API."""
    # Настраиваем поведение для этого теста
    mock_requests_get.side_effect = requests.exceptions.RequestException("Connection error")

    with pytest.raises(requests.exceptions.RequestException):
        hh_api._connect_api()
    assert hh_api.is_connected is False
    mock_requests_get.assert_called_once()  # Проверяем, что была попытка вызова


def test_load_vacancies_success(hh_api, mock_requests_get):
    """Успешная загрузка вакансий: проверяем, что собираются вакансии со всех страниц."""
    hh_api._connected = True  # Мокируем успешное подключение

    # Настраиваем возвращаемое значение для mock_requests_get
    # Каждый раз возвращаем 2 вакансии
    mock_requests_get.return_value.json.return_value = {
        "items": [{"id": 1, "name": "Vacancy 1"}, {"id": 2, "name": "Vacancy 2"}]
    }

    hh_api.load_vacancies("Python", per_page=2)
    vacancies = hh_api.get_vacancies()

    # Ожидаем 20 страниц * 2 вакансии на каждой = 40 вакансий
    expected_total_vacancies = 20 * 2
    assert len(vacancies) == expected_total_vacancies

    # Также убедимся, что requests.get был вызван 20 раз (для каждой страницы)
    assert mock_requests_get.call_count == 20


def test_load_vacancies_not_connected(hh_api, mocker, capsys):  # Здесь mocker нужен для mocker.patch.object
    """Проверяем, что происходит, если не удалось подключиться."""
    # Используем mocker.patch.object() - он сам позаботится об очистке
    mocker.patch.object(hh_api, "_connect_api", side_effect=Exception("Connection failed"))

    hh_api.load_vacancies("Python")
    captured = capsys.readouterr()
    assert "Не удалось подключиться к API" in captured.out
    assert hh_api.get_vacancies() == []


def test_set_params_text(hh_api):
    """Проверяем сеттер параметра text."""
    hh_api.set_params_text("test")
    assert hh_api.params["text"] == "test"


def test_set_get_url(hh_api):
    """Проверяем сеттер и геттер параметра url."""
    hh_api.url = "https://"
    assert hh_api.url == "https://"


def test_set_get_params(hh_api):
    """Проверяем сеттер и геттер параметров."""
    hh_api.params = {"text": "t", "page": 1, "per_page": 20, "area": 113}
    assert hh_api.params == {"text": "t", "page": 1, "per_page": 20, "area": 113}
