import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import requests


class ApiVacancies(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Инициализация с общим ключом API (если требуется)."""
        self._api_key: Optional[str] = api_key  # Защищенный атрибут
        self._connected: bool = False  # Атрибут для отображения коннекта к АПИ

    @abstractmethod
    def load_vacancies(self, keyword: str) -> None:
        """Метод для загрузки вакансий по ключевому слову."""
        pass

    @abstractmethod
    def _connect_api(self) -> None:
        """Приватный метод для подключения к API hh.ru."""
        pass

    @property
    def api_key(self) -> Optional[str]:
        """Геттер для api_key."""
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: Optional[str]) -> None:
        """Сеттер для api_key."""
        self._api_key = api_key

    @property
    def is_connected(self) -> bool:
        """Геттер для статуса подключения к апи."""
        return self._connected


class VacanciesHh(ApiVacancies):
    """Класс, наследующийся от абстрактного класса, для работы с платформой hh.ru."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Функция инициализации атрибутов."""
        super().__init__(api_key)
        self.__url: str = "https://api.hh.ru/vacancies"
        self.__headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        }
        self.__params: Dict[str, Any] = {"text": "", "page": 0, "per_page": 100, "area": 113}
        self.__vacancies_data: List[Dict[str, Any]] = []

    def _connect_api(self) -> None:
        """Приватный метод для подключения к API hh.ru."""
        try:
            response = requests.get(self.__url, headers=self.__headers)
            response.raise_for_status()
            self._connected = True  # Устанавливаем флаг в родительском классе
            print("Успешно подключились к API hh.ru")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при подключении к API hh.ru: {e}")
            self._connected = False  # Устанавливаем флаг в родительском классе
            raise  # Re-raise exception чтобы указать на невозможность продолжения работы

    def load_vacancies(self, keyword: str, per_page: int = 10) -> None:
        """Загрузка вакансий с hh.ru по ключевому слову."""
        if not self.is_connected:  # Используем геттер родительского класса
            try:  # Пытаемся подключиться к АПИ
                self._connect_api()  # вызываем protected метод
            except Exception:
                print("Не удалось подключиться к API. Загрузка вакансий невозможна.")
                return

        self.__params["text"] = keyword
        self.__params["page"] = 0  # Начинаем с первой страницы
        self.__params["per_page"] = per_page  # Устанавливаем per_page(количество объектов)
        self.__vacancies_data = []

        while self.__params.get("page") != 20:  # Лимит в 20 страниц
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                vacancies: List[Dict[str, Any]] = response.json()["items"]
                self.__vacancies_data.extend(vacancies)
                self.__params["page"] += 1
                time.sleep(0.5)  # Задержка

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к API: {e}")
                break

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """Геттер для списка вакансий."""
        return self.__vacancies_data

    # Геттеры и сеттеры для других атрибутов (по необходимости)
    @property
    def url(self) -> str:
        """Геттер для url."""
        return self.__url

    @url.setter
    def url(self, new_url: str) -> None:
        """Сеттер для url."""
        self.__url = new_url

    @property
    def params(self) -> Dict[str, Any]:
        """Геттер для параметров."""
        return self.__params

    @params.setter
    def params(self, new_params: Dict[str, Any]) -> None:
        """Cеттер для параметров."""
        self.__params = new_params

    def set_params_text(self, text: str) -> None:
        """Сеттер для изменения текста."""
        self.__params["text"] = text


# # Пример использования:
# if __name__ == "__main__":
#     hh_api = VacanciesHh()
#     try:
#         hh_api._connect_api()  # Сначала подключаемся к API
#         hh_api.load_vacancies("Python")
#         vacancies = hh_api.get_vacancies()
#
#         if vacancies:
#             print(f"Найдено {len(vacancies)} вакансий.")
#             # Дальнейшая обработка вакансий
#             for vacancy in vacancies:
#                 print(vacancy)  # Пример вывода названий вакансий ['name'])
#         else:
#             print("Не удалось загрузить вакансии.")
#     except requests.exceptions.RequestException:
#         print("Не удалось выполнить запрос из-за проблем с подключением к API.")
