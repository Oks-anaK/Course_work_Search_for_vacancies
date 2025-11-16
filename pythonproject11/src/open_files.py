import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, cast


class Handler(ABC):
    """Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях."""

    def __init__(self, filename: str) -> None:
        """Функция инициализации атрибутов."""
        pass

    @abstractmethod
    def read_vacancies(self) -> List[Dict[str, Any]]:
        """Функция чтения вакансий."""
        pass

    @abstractmethod
    def add_vacancies(self, data_to_add: Iterable[Dict[str, Any]]) -> None:
        """Функция добавления вакансий."""
        pass

    @abstractmethod
    def remove_vacancies(self, criteria: Callable[[Dict[str, Any]], bool]) -> None:
        """Функция удаления вакансий."""
        pass


class JsonHandler(Handler):
    """Класс, наследующийся от абстрактного класса, для добавления, чтения, удаления информации
    о вакансиях в JSON-файл."""

    def __init__(self, filename: str = "vacancies.json") -> None:
        """Функция инициализации атрибутов."""
        super().__init__(filename)
        self.__filename = filename

    def read_vacancies(self) -> Any:
        """Функция чтения вакансий в json."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_vacancies(self, data_to_add: Iterable[Dict[str, Any]]) -> None:
        """Функция добавления новых вакансий в json."""
        try:
            data = self.read_vacancies()
            existing_urls = {vacancy["url"] for vacancy in data if "url" in vacancy}

            unique_new_vacancies = []
            seen_urls_in_this_batch = set()

            for vacancy in data_to_add:
                url = vacancy.get("url")
                if url:
                    if url not in existing_urls and url not in seen_urls_in_this_batch:
                        unique_new_vacancies.append(vacancy)
                        seen_urls_in_this_batch.add(url)
                else:
                    unique_new_vacancies.append(vacancy)

            data.extend(unique_new_vacancies)
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")

    def remove_vacancies(self, criteria: Callable[[Dict[str, Any]], bool]) -> None:
        """Функция удаления вакансий из json."""
        try:
            data = self.read_vacancies()
            updated_data = [vacancy for vacancy in data if not criteria(vacancy)]
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")


# # Пример функции критериев удаления по url
# def criteria_func(vacancy):
#     return vacancy.get("url") == "https://example.com/python-developer"


# if __name__ == "__main__":
#     filename = "vacancies.json"
#     json_handler = JsonHandler(filename)
#
#     new_vacancies = [
#         {"url": "https://example.com/python-developer", "title": "Python Developer", "company": "Google"},
#         {"url": "https://example.com/data-scientist", "title": "Data Scientist", "company": "Microsoft"},
#         {
#             "url": "https://example.com/python-developer",
#             "title": "Python Developer",
#             "company": "Google",
#         },  # Дубликат по url
#     ]
#
#     json_handler.add_vacancies(new_vacancies)
#     vacancies = json_handler.read_vacancies()
#     print("Вакансии после добавления:", vacancies)
#
#     json_handler.remove_vacancies(criteria_func)  # Удаление вакансии по url
#     vacancies = json_handler.read_vacancies()
#     print("Вакансии после удаления:", vacancies)
