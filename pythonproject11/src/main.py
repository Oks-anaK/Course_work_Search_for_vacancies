# def user_interaction():
#     platforms = ["HeadHunter"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#
#     [print(v) for v in sorted(_list, reverse=True)]
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
#
#


# if __name__ == "__main__":
#     user_interaction()
import requests
from pythonproject11.src.api_connect import VacanciesHh
from pythonproject11.src.vacancies import Vacancy
from pythonproject11.src.open_files import JsonHandler

def get_vacancy_description(vacancy_url):
    """Получает описание вакансии по URL."""
    try:
        response = requests.get(vacancy_url)
        response.raise_for_status()
        vacancy_data = response.json()
        return vacancy_data.get('description', 'Описание не указано')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении информации о вакансии: {e}")
        return "Описание не удалось загрузить"

def extract_salary(salary_data):
    """Извлекает данные о зарплате."""
    salary_from = salary_data.get('from') if salary_data else None
    salary_to = salary_data.get('to') if salary_data else None
    return salary_from, salary_to

def create_vacancy_objects(vacancies_data):
    """Создает список объектов Vacancy."""
    vacancies = []
    for data in vacancies_data:
        title = data.get('name', 'Название не указано')
        url = data.get('alternate_url', 'URL не указан')
        salary_from, salary_to = extract_salary(data.get('salary'))
        description = get_vacancy_description(data.get('url'))
        vacancy = Vacancy(title, url, salary_from, salary_to, description)
        vacancies.append(vacancy)
    return vacancies

def main():
    hh = VacanciesHh()
    hh.connect_api()
    hh.load_vacancies("Python")
    vacancies_data = hh.get_vacancies()

    vacancies = create_vacancy_objects(vacancies_data)

    [print(v) for v in sorted(vacancies, reverse=True)[:5]]

    filename = 'vacancies.json'
    json_handler = JsonHandler(filename)

    json_handler.add_vacancies(vacancies)

    new_vacancies = json_handler.read_vacancies()

if __name__ == '__main__':
    main()

