from typing import Optional

from pythonproject11.src.api_connect import VacanciesHh
from pythonproject11.src.open_files import JsonHandler
from pythonproject11.src.processing_data import create_vacancy_objects


def main() -> None:
    """Основная функция для выполнения поиска вакансий,
    взаимодействия с API, обработки данных и сохранения в файл."""

    user_keyword: Optional[str] = None
    user_number_vacancies: Optional[int] = None

    try:
        user_keyword = str(input("Введите необходимое слово для поиска по вакансиям: "))
        user_number_vacancies = int(
            input("Введите количество вакансий, которые вы хотите получить (не менее 20 и не более 2000): ")
        )
    except (ValueError, TypeError):
        print("Неправильный ввод. Попробуйте снова.")
        return

    hh_api = VacanciesHh()
    hh_api._connect_api()  # Сначала подключаемся к API

    if 20 <= user_number_vacancies <= 2000:  # Проверяем введенное значение
        user_number_vacancies_valid = round(user_number_vacancies / 20)

        hh_api.load_vacancies(user_keyword, per_page=user_number_vacancies_valid)
        vacancies_data = hh_api.get_vacancies()

    else:
        print("Запрос превысил доступный диапазон (от 20 до 2000). Попробуйте снова.")
        return

    vacancies = create_vacancy_objects(vacancies_data)

    vacancies_to_add = [vacancy.cast_to_dict() for vacancy in vacancies]

    filename = "vacancies.json"
    json_handler = JsonHandler(filename)

    json_handler.add_vacancies(vacancies_to_add)

    new_vacancies = json_handler.read_vacancies()
    print(new_vacancies)


# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         print(f"Возникли проблемы с функцией main {e}.")
