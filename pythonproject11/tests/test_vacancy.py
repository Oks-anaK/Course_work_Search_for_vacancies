import pytest

from pythonproject11.src.vacancy import Vacancy


def test_init_and_attributes():
    """Тест на инициализацию."""
    concrete_v = Vacancy("Title", "http://url", 10, 20, "Descr")
    assert concrete_v.title == "Title"
    assert concrete_v.url == "http://url"
    assert concrete_v.description == "Descr"
    assert concrete_v.salary == 15


def test_slots_prevent_adding_new_attribute():
    """Тест на препятствие добавления в slots нового атрибута."""
    concrete_v = Vacancy("T", "U", None, None, "D")
    with pytest.raises(AttributeError):
        concrete_v.new_attribute = 123  # __slots__ запрещает динамическое добавление


@pytest.mark.parametrize(
    "salary_from,salary_to,expected",
    [
        (10, 20, 15),
        (5.5, 6.5, 6.0),
        (0, 0, 0),
        (-10, -20, -15),  # проверяем отрицательные значения (поведение: арифметика работает)
    ],
)
def test_validate_both_salary(salary_from, salary_to, expected):
    """Тест на вычисление средней зарплаты и валидацию с двумя зарплатами."""
    v = Vacancy("t", "u", salary_from, salary_to, "d")
    assert v.salary == expected


@pytest.mark.parametrize(
    "salary_from, salary_to, expected",
    [
        (None, 10, 10),
        (15, None, 15),
        (None, None, 0),
    ],
)
def test_validate_single_or_none_salary(salary_from, salary_to, expected):
    """Тест на вычисление средней зарплаты и валидацию с одной None или двумя None зарплатами."""
    v = Vacancy("t", "u", salary_from, salary_to, "d")
    assert v.salary == expected


@pytest.mark.parametrize(
    "salary_from, salary_to",
    [
        ([3], "apple"),
        ("100", 1000),
        (2000, [234]),
        ([1, 2], None),
        (None, {"x": 1}),
    ],
)
def test_validate_invalid_types_raise_value_error(salary_from, salary_to):
    """Тест на вычисление средней зарплаты и валидацию с недопустимями значениями зарплат."""
    with pytest.raises(ValueError):
        Vacancy("t", "u", salary_from, salary_to, "d")


def test_salary_setter_and_getter():
    """Тест на сеттер и геттер зарплаты."""
    v = Vacancy("t", "u", 5, None, "d")
    assert v.salary == 5
    v.salary = 100
    assert v.salary == 100
    v.salary = "not a number"
    assert v.salary == 0  # сеттер ставит 0 для неверного типа


def test_comparisons_between_vacancies():
    """Тест на сравнение вакансий по зарплате."""

    low = Vacancy("low", "u", 10, 10, "d")
    mid = Vacancy("mid", "u", 15, 15, "d")
    high = Vacancy("high", "u", 30, 30, "d")

    assert low < mid
    assert low <= mid
    assert high > mid
    assert high >= mid
    assert mid == Vacancy("another mid", "url", 10, 20, "desc")


def test_comparison_with_other_types():
    """Тест на сравнение вакансий с разными типами данных."""
    v = Vacancy("t", "u", 10, 10, "")
    # для eq возвращается False при сравнении с другим типом
    assert (v == 123) is False
    # остальные операции должны поднимать ValueError
    with pytest.raises(ValueError):
        _ = v < 123
    with pytest.raises(ValueError):
        _ = v > "string"
    with pytest.raises(ValueError):
        _ = v <= []
    with pytest.raises(ValueError):
        _ = v >= object()


def test_str_and_repr_and_cast_to_dict():
    """Тест на успешное выполнение методов str, repr, cast_to_dict."""
    v = Vacancy("MyTitle", "http://", 7, 9, "Описание")
    s = str(v)
    r = repr(v)
    d = v.cast_to_dict()

    assert "Название:" in s
    assert "зарплата" in s
    assert "Vacancy(" in r
    assert "salary=" in r

    assert isinstance(d, dict)
    assert d["title"] == "MyTitle"
    assert d["url"] == "http://"
    assert d["description"] == "Описание"
    assert d["salary"] == v.salary
