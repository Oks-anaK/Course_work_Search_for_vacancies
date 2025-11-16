from pythonproject11.src.main import main


# Мокаем класс Vacancy, который создается функцией create_vacancy_objects
# и используется для вызова метода cast_to_dict().
class MockVacancy:
    """Мок-класс для объекта вакансии, имитирующий метод cast_to_dict."""

    def __init__(self, data):
        self.data = data

    def cast_to_dict(self):
        """Имитирует преобразование объекта вакансии в словарь."""
        return self.data


def test_main_successful_execution(mock_modules, capfd):
    """
    Тест успешного выполнения main с корректным вводом:
    - ввод: "Python", "100"
    - ожидаем, что hh_api._connect_api вызван,
      load_vacancies вызван с per_page=5 (100/20 = 5),
      и что в консоль выведен результат read_vacancies.
    """
    mock_modules["input"].side_effect = ["Python", "100"]

    mock_vacancies_data_from_api = [{"id": "123", "name": "Dev"}]
    mock_vacancy_objects = [MockVacancy({"id": "123", "name": "Dev"})]
    mock_read_vacancies_result = [{"id": "123", "name": "Dev", "source": "json"}]

    mock_modules["hh_api_instance"].get_vacancies.return_value = mock_vacancies_data_from_api
    mock_modules["create_vacancy_objects"].return_value = mock_vacancy_objects
    mock_modules["json_handler_instance"].read_vacancies.return_value = mock_read_vacancies_result

    # Вызов тестируемой функции
    main()

    # Проверки вызовов input
    mock_modules["input"].assert_any_call("Введите необходимое слово для поиска по вакансиям: ")
    mock_modules["input"].assert_any_call(
        "Введите количество вакансий, которые вы хотите получить (не менее 20 и не более 2000): "
    )

    # Проверки вызовов API и обработки
    mock_modules["hh_api_instance"]._connect_api.assert_called_once()
    mock_modules["hh_api_instance"].load_vacancies.assert_called_once_with("Python", per_page=5)
    mock_modules["hh_api_instance"].get_vacancies.assert_called_once()
    mock_modules["create_vacancy_objects"].assert_called_once_with(mock_vacancies_data_from_api)

    # Проверки JSON-хендлера
    mock_modules["json_handler_instance"].add_vacancies.assert_called_once_with([{"id": "123", "name": "Dev"}])
    mock_modules["json_handler_instance"].read_vacancies.assert_called_once()

    # Проверка вывода в консоль (capfd)
    out, err = capfd.readouterr()
    assert out.strip() == str(mock_read_vacancies_result)


def test_main_invalid_number_input_type(mock_modules, capfd):
    """
    Тест сценария нечислового ввода количества вакансий.
    Поскольку в текущей реализации main ловит TypeError,
    мы симулируем ситуацию TypeError при втором input, чтобы main поймал исключение
    и вывел сообщение, которое реализовано в main.
    """
    # Симулируем, что второй вызов input вызовет TypeError (чтобы попасть в except TypeError)
    mock_modules["input"].side_effect = ["Python", TypeError("simulated type error")]

    main()

    # Ожидаемое сообщение в текущей реализации main
    out, err = capfd.readouterr()
    assert "Неправильный ввод. Попробуйте снова." in out

    # При этом API и дальнейшие шаги не должны были быть вызваны
    mock_modules["hh_api_instance"]._connect_api.assert_not_called()
    mock_modules["hh_api_instance"].load_vacancies.assert_not_called()
    mock_modules["json_handler_instance"].add_vacancies.assert_not_called()
    mock_modules["create_vacancy_objects"].assert_not_called()


def test_main_number_out_of_range_low(mock_modules, capfd):
    """
    Тест случая, когда запрошенное количество < 20.
    В текущей реализации соединение с API происходит перед проверкой диапазона,
    поэтому ожидаем, что _connect_api будет вызван, а затем выведется сообщение о диапазоне.
    """
    mock_modules["input"].side_effect = ["Java", "15"]

    main()

    mock_modules["hh_api_instance"]._connect_api.assert_called_once()
    out, err = capfd.readouterr()
    assert "Запрос превысил доступный диапазон" in out

    # Никаких загрузок и добавлений в JSON быть не должно
    mock_modules["hh_api_instance"].load_vacancies.assert_not_called()
    mock_modules["json_handler_instance"].add_vacancies.assert_not_called()
    mock_modules["create_vacancy_objects"].assert_not_called()


def test_main_number_out_of_range_high(mock_modules, capfd):
    """
    Тест случая, когда запрошенное количество > 2000.
    Аналогично, соединение с API ожидается перед проверкой диапазона.
    """
    mock_modules["input"].side_effect = ["Go", "2500"]

    main()

    mock_modules["hh_api_instance"]._connect_api.assert_called_once()
    out, err = capfd.readouterr()
    assert "Запрос превысил доступный диапазон" in out

    mock_modules["hh_api_instance"].load_vacancies.assert_not_called()
    mock_modules["json_handler_instance"].add_vacancies.assert_not_called()
    mock_modules["create_vacancy_objects"].assert_not_called()


def test_main_empty_vacancies_from_api(mock_modules, capfd):
    """
    Тест случая, когда API возвращает пустой список вакансий.
    Ожидаем, что обработка пройдет, JSON сохранит пустой список, и произойдет вывод пустого списка.
    """
    mock_modules["input"].side_effect = ["NoResults", "40"]

    mock_vacancies_data_from_api = []
    mock_vacancy_objects = []
    mock_read_vacancies_result = []

    mock_modules["hh_api_instance"].get_vacancies.return_value = mock_vacancies_data_from_api
    mock_modules["create_vacancy_objects"].return_value = mock_vacancy_objects
    mock_modules["json_handler_instance"].read_vacancies.return_value = mock_read_vacancies_result

    main()

    mock_modules["hh_api_instance"]._connect_api.assert_called_once()
    mock_modules["hh_api_instance"].load_vacancies.assert_called_once_with("NoResults", per_page=2)  # 40/20=2
    mock_modules["hh_api_instance"].get_vacancies.assert_called_once()
    mock_modules["create_vacancy_objects"].assert_called_once_with([])
    mock_modules["json_handler_instance"].add_vacancies.assert_called_once_with([])
    mock_modules["json_handler_instance"].read_vacancies.assert_called_once()

    out, err = capfd.readouterr()
    assert out.strip() == "[]"
