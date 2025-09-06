from abc import ABC, abstractmethod
import requests

class ApiVacancies(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    def __init__(self, api_key=None):
        """Инициализация с общим ключом API (если требуется)."""
        self.api_key = api_key  # Сохраняем API-ключ (если передан)

    @abstractmethod
    def connect_api(self):
        """Метод для подключения к API."""
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        """Метод для загрузки вакансий по ключевому слову."""
        pass


class VacanciesHh(ApiVacancies):
    """Класс для работы с платформой hh.ru."""

    def __init__(self, api_key=None):
        """Инициализация параметров для HH.ru."""
        super().__init__(api_key)
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100, 'area': 113} #Добавил параметр area - вся Россия
        self.vacancies_data = [] #Переименовал vacancies в vacancies_data чтобы отличать от списка объектов Vacancy
        self.connected = False  # Флаг, показывающий, что подключение установлено

    def connect_api(self):
        """Подключение к API hh.ru."""
        try:
            #Проверим доступность API:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.connected = True  # Устанавливаем флаг, если подключение успешно
            print("Успешно подключились к API hh.ru")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при подключении к API hh.ru: {e}")
            self.connected = False
            raise  # Re-raise exception чтобы указать на невозможность продолжения работы

    def load_vacancies(self, keyword):
        """Загрузка вакансий с hh.ru по ключевому слову."""
        if not self.connected:
            print("Необходимо сначала подключиться к API (вызвать connect_api)")
            return  # Выходим, если не подключены

        self.params['text'] = keyword
        self.params['page'] = 0  # сбрасываем страницу на 0 при каждом запросе вакансий по новому ключевому слову
        self.vacancies_data = []  # очищаем предыдущие вакансии при каждом запросе по новому ключевому слову

        while self.params.get('page') != 20:
            try:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                response.raise_for_status()
                vacancies = response.json()['items']
                self.vacancies_data.extend(vacancies)
                self.params['page'] += 1
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                break  # Прерываем цикл при ошибке

    def get_vacancies(self):
        return self.vacancies_data

# Пример использования:
if __name__ == '__main__':
    hh_api = VacanciesHh()
    try:
        hh_api.connect_api()  # Сначала подключаемся к API
        hh_api.load_vacancies("Python")
        vacancies = hh_api.get_vacancies()

        if vacancies:
            print(f"Найдено {len(vacancies)} вакансий.")
            # Дальнейшая обработка вакансий
            for vacancy in vacancies:
                print(vacancy['name']) # Пример вывода названий вакансий
        else:
            print("Не удалось загрузить вакансии.")
    except requests.exceptions.RequestException:
        print("Не удалось выполнить запрос из-за проблем с подключением к API.")