from pythonproject11.src import processing_data


def test_clean_html_to_text_none_and_empty():
    """Тест на чистку пустой строки и None."""
    assert processing_data.clean_html_to_text(None) == ""
    assert processing_data.clean_html_to_text("") == ""


def test_clean_html_to_text_basic_html():
    """Тест на базовый html."""
    html = "<p>Hello <b>world</b></p>"
    assert processing_data.clean_html_to_text(html) == "Hello world"


def test_clean_html_to_text_nested():
    """Тест на чистку html с вложенным текстом."""
    html = "<div>Просто текст<br><span>и <em>выделение</em></span></div>"
    expected_result = "Просто текст и выделение"

    # Преобразуем HTML-код, заменяя   на нормальный пробел
    cleaned_html = html.replace(" ", " ")
    result = processing_data.clean_html_to_text(cleaned_html)

    assert result == expected_result


def test_create_vacancy_objects_full(monkeypatch, simple_class):
    """Тест с похожим на Vacancy классом."""
    # Подменяем оригинальный Vacancy на простой класс для тестирования
    monkeypatch.setattr(processing_data, "Vacancy", simple_class)

    data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://example.com/job/1",
            "salary": {"from": 100000, "to": 200000},
            "snippet": {"requirement": "<p>Опыт в Django</p>", "responsibility": "<div>Разработка API</div>"},
        }
    ]

    result = processing_data.create_vacancy_objects(data)
    assert len(result) == 1
    vac = result[0]
    assert vac.title == "Python Developer"
    assert vac.url == "https://example.com/job/1"
    assert vac.salary_from == 100000
    assert vac.salary_to == 200000
    assert "Требования: Опыт в Django." in vac.description
    assert "Обязанности: Разработка API" in vac.description


def test_create_vacancy_objects_missing_snippet(monkeypatch, simple_class):
    """Тест с вакансией без snippet."""
    monkeypatch.setattr(processing_data, "Vacancy", simple_class)

    data = [
        {
            "name": "No Snippet",
            "alternate_url": "https://example.com/job/2",
            # snippet отсутствует
        }
    ]

    result = processing_data.create_vacancy_objects(data)
    assert len(result) == 1
    vac = result[0]
    assert vac.description == ""


def test_create_vacancy_objects_missing_salary(monkeypatch, simple_class):
    """Тест с вакансией без зарплаты."""
    monkeypatch.setattr(processing_data, "Vacancy", simple_class)

    data = [
        {
            "name": "No Salary",
            "alternate_url": "https://example.com/job/3",
            # salary отсутствует
            "snippet": {"requirement": "req", "responsibility": "resp"},
        }
    ]

    result = processing_data.create_vacancy_objects(data)
    vac = result[0]
    # после правки функции ожидаем None для from/to
    assert vac.salary_from is None
    assert vac.salary_to is None
