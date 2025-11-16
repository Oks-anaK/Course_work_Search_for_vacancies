from unittest.mock import mock_open  # Для имитации ошибок ввода/вывода


# --- Тесты для JsonHandler ---
def test_initialization_with_default_filename(json_handler):
    """Проверка инициализации JsonHandler с именем файла по умолчанию."""
    # Фикстура json_handler уже проверяет существование и удаление файла.
    # Поэтому мы в основном проверяем, что внутреннее имя файла установлено правильно.
    # Обращение к приватному полю для целей тестирования, хотя это не является идеальной практикой в продакшн-коде.
    assert json_handler._JsonHandler__filename == "test_vacancies.json"


def test_read_vacancies_empty_file(json_handler):
    """Проверка чтения из пустого или несуществующего файла."""
    assert json_handler.read_vacancies() == []


def test_read_vacancies_with_data(json_handler, sample_vacancies):
    """Проверка чтения вакансий после их добавления."""
    json_handler.add_vacancies(sample_vacancies)
    read_data = json_handler.read_vacancies()
    assert len(read_data) == len(sample_vacancies)
    # Проверить, что прочитанные данные соответствуют записанным
    for vacancy in sample_vacancies:
        assert vacancy in read_data


def test_read_vacancies_malformed_json(json_handler):
    """Проверка чтения из файла с некорректными JSON-данными, ожидается пустой список."""
    filename = json_handler._JsonHandler__filename
    # Записать некорректный JSON в тестовый файл
    with open(filename, "w", encoding="utf-8") as f:
        f.write("{ 'key': 'value', 'bad_json_ending")  # Намеренно некорректный JSON

    read_data = json_handler.read_vacancies()
    assert read_data == []


def test_add_vacancies_to_empty_file(json_handler, sample_vacancies):
    """Проверка добавления вакансий в изначально пустой файл."""
    json_handler.add_vacancies(sample_vacancies)
    read_data = json_handler.read_vacancies()
    assert len(read_data) == len(sample_vacancies)
    # Проверить содержимое
    for vacancy in sample_vacancies:
        assert vacancy in read_data


def test_add_vacancies_with_duplicates(json_handler, sample_vacancies_with_duplicates):
    """Проверка добавления вакансий, убеждаясь, что дублирующиеся URL не добавляются."""
    initial_vacancies = [{"url": "https://example.com/initial", "title": "Initial Role", "company": "InitialCorp"}]
    json_handler.add_vacancies(initial_vacancies)

    json_handler.add_vacancies(sample_vacancies_with_duplicates)
    read_data = json_handler.read_vacancies()

    # Ожидаемые уникальные вакансии: начальные + уникальные из sample_vacancies_with_duplicates
    expected_unique_urls = {
        "https://example.com/initial",
        "https://example.com/python-developer",
        "https://example.com/data-scientist",
        "https://example.com/java-developer",
    }
    actual_urls = {vacancy.get("url") for vacancy in read_data if "url" in vacancy}  # Отфильтровать вакансии с URL

    assert len(actual_urls) == len(expected_unique_urls)  # сравнение множеств
    assert actual_urls == expected_unique_urls  # сравнение множеств

    # Также проверить общее количество вакансий (включая те, что без URL, если они были добавлены)
    # В этой конкретной фикстуре все вакансии имеют URL, поэтому len(read_data) должно соответствовать
    # expected_unique_urls + len(initial_vacancies)
    assert len(read_data) == len(expected_unique_urls)  # было == len(expected_unique_urls) + len(initial_vacancies)


def test_add_vacancies_without_url(json_handler, sample_vacancies_without_url):
    """Проверка добавления вакансий, некоторые из которых без поля 'url'.
    Все они должны быть добавлены, так как не могут считаться дубликатами по URL."""
    json_handler.add_vacancies(sample_vacancies_without_url)
    read_data = json_handler.read_vacancies()

    # Проверить содержимое
    for vacancy in sample_vacancies_without_url:
        assert vacancy in read_data

    # Добавить их снова, чтобы убедиться в идемпотентности для элементов без URL
    json_handler.add_vacancies(sample_vacancies_without_url)
    read_data_after_second_add = json_handler.read_vacancies()

    # Количество вакансий увеличится на количество вакансий без URL
    vacancies_without_url_count = sum(1 for v in sample_vacancies_without_url if "url" not in v)
    assert len(read_data_after_second_add) == len(sample_vacancies_without_url) + vacancies_without_url_count


def test_add_empty_list_of_vacancies(json_handler, sample_vacancies):
    """Проверка добавления пустого списка вакансий. Не должно менять данные."""
    json_handler.add_vacancies(sample_vacancies)
    initial_data = json_handler.read_vacancies()

    json_handler.add_vacancies([])
    read_data = json_handler.read_vacancies()

    assert read_data == initial_data
    assert len(read_data) == len(initial_data)


def test_add_vacancies_idempotency(json_handler, sample_vacancies):
    """Проверка того, что многократное добавление одних и тех же вакансий не изменяет их количество."""
    json_handler.add_vacancies(sample_vacancies)
    initial_count = len(json_handler.read_vacancies())

    json_handler.add_vacancies(sample_vacancies)
    second_read_data = json_handler.read_vacancies()
    assert len(second_read_data) == initial_count
    for vacancy in sample_vacancies:
        assert vacancy in second_read_data


def test_add_vacancies_io_error(json_handler, sample_vacancies, mocker):
    """Проверка add_vacancies при возникновении IOError во время записи файла."""
    # Успешно добавить начальные данные
    json_handler.add_vacancies([{"url": "initial.com", "title": "Init", "company": "InitCorp"}])
    initial_data = json_handler.read_vacancies()

    # Имитировать open, чтобы вызвать IOError при попытке записи ('w')
    # Создаем мок файлового объекта
    mock_file_obj = mock_open()
    # Устанавливаем side_effect для метода write этого мока
    mock_file_obj.return_value.write.side_effect = IOError("Permission denied")
    mocker.patch("builtins.open", mock_file_obj)  # Применяем мок к builtins.open

    json_handler.add_vacancies(sample_vacancies)

    mocker.stopall()
    current_data = json_handler.read_vacancies()
    assert current_data == initial_data


def test_remove_vacancies_by_url(json_handler, sample_vacancies, criteria_to_remove_one):
    """Проверка удаления одной вакансии по критерию URL."""
    json_handler.add_vacancies(sample_vacancies)
    initial_data = json_handler.read_vacancies()
    assert len(initial_data) == 3

    json_handler.remove_vacancies(criteria_to_remove_one)
    read_data = json_handler.read_vacancies()

    # Проверить, что конкретная вакансия была удалена
    removed_vacancy_url = "https://example.com/python-developer"
    assert not any(v.get("url") == removed_vacancy_url for v in read_data)
    # Проверить, что остальные вакансии остались
    assert len(read_data) == 2
    assert {
        "url": "https://example.com/data-scientist",
        "title": "Data Scientist",
        "company": "Microsoft",
    } in read_data
    assert {"url": "https://example.com/java-developer", "title": "Java Developer", "company": "Amazon"} in read_data


def test_remove_vacancies_by_company(json_handler, sample_vacancies, criteria_to_remove_multiple):
    """Тестирование удаления нескольких вакансий в зависимости от названия компании."""
    # Добавить начальные данные
    json_handler.add_vacancies(sample_vacancies)  # 3 вакансии: Google, Microsoft, Amazon

    # Добавить больше данных, где несколько записей соответствуют критериям (Microsoft)
    data_to_add = [
        {"url": "https://example.com/ml-engineer", "title": "ML Engineer", "company": "Microsoft"},
        {"url": "https://example.com/frontend-dev", "title": "Frontend Developer", "company": "Google"},
        {"url": "https://example.com/backend-dev", "title": "Backend Developer", "company": "Microsoft"},
    ]
    json_handler.add_vacancies(data_to_add)  # + 3 уникальные вакансии: Microsoft, Google, Microsoft

    initial_data = json_handler.read_vacancies()
    # Всего уникальных вакансий: 6
    # 1. Python Developer (Google)
    # 2. Data Scientist (Microsoft)
    # 3. Java Developer (Amazon)
    # 4. ML Engineer (Microsoft)
    # 5. Frontend Developer (Google)
    # 6. Backend Developer (Microsoft)
    assert len(initial_data) == 6

    json_handler.remove_vacancies(criteria_to_remove_multiple)  # Удалить все вакансии "Microsoft"
    read_data = json_handler.read_vacancies()

    # Ожидаемое количество оставшихся: 6 - 3 (Microsoft) = 3 вакансии
    # 1. Python Developer (Google)
    # 2. Java Developer (Amazon)
    # 3. Frontend Developer (Google)
    assert len(read_data) == 3
    assert not any(v.get("company") == "Microsoft" for v in read_data)
    assert {"url": "https://example.com/frontend-dev", "title": "Frontend Developer", "company": "Google"} in read_data


def test_remove_vacancies_no_match(json_handler, sample_vacancies, criteria_no_match):
    """Проверка удаления вакансий, когда критерии ничего не находят."""
    json_handler.add_vacancies(sample_vacancies)
    initial_data = json_handler.read_vacancies()
    initial_count = len(initial_data)

    json_handler.remove_vacancies(criteria_no_match)
    read_data = json_handler.read_vacancies()

    # Убедиться, что ни одна вакансия не была удалена
    assert len(read_data) == initial_count
    assert read_data == initial_data


def test_remove_vacancies_empty_file(json_handler, criteria_to_remove_one):
    """Проверка удаления вакансий из пустого файла."""
    # Файл пуст благодаря настройке фикстуры
    json_handler.remove_vacancies(criteria_to_remove_one)
    read_data = json_handler.read_vacancies()
    assert read_data == []


def test_remove_vacancies_io_error(json_handler, sample_vacancies, mocker):
    """Проверка remove_vacancies при возникновении IOError во время записи файла."""
    json_handler.add_vacancies(sample_vacancies)
    initial_data = json_handler.read_vacancies()
    initial_count = len(initial_data)

    # Имитировать open, чтобы вызвать IOError при попытке записи ('w')
    # Создаем мок файлового объекта
    mock_file_obj = mock_open()
    # Устанавливаем side_effect для метода write этого мока
    mock_file_obj.return_value.write.side_effect = IOError("Disk full")
    mocker.patch("builtins.open", mock_file_obj)  # Применяем мок к builtins.open

    json_handler.remove_vacancies(lambda v: v.get("company") == "Microsoft")

    mocker.stopall()
    current_data = json_handler.read_vacancies()
    assert current_data == initial_data
    assert len(current_data) == initial_count


def test_remove_vacancies_criteria_raises_error(json_handler, sample_vacancies, criteria_raises_error, capsys):
    """Проверка remove_vacancies, когда сама функция критериев генерирует исключение."""
    json_handler.add_vacancies(sample_vacancies)
    initial_data = json_handler.read_vacancies()
    initial_count = len(initial_data)

    # Вызвать remove_vacancies с критерием, который генерирует ошибку
    json_handler.remove_vacancies(criteria_raises_error)

    # Содержимое файла не должно было измениться, потому что ошибка в критериях
    # должна предотвратить успешное завершение операции записи.
    read_data = json_handler.read_vacancies()
    assert read_data == initial_data
    assert len(read_data) == initial_count

    # При желании, проверить, что сообщение об ошибке было выведено
    captured = capsys.readouterr()
    assert "Ошибка: Criteria function encountered an error!" in captured.out
