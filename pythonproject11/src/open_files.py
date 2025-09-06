from abc import ABC, abstractmethod
import json

class Handler(ABC):
    """Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях."""

    @abstractmethod
    def __init__(self, filename):
        pass

    @abstractmethod
    def read_vacancies(self):
        pass

    @abstractmethod
    def add_vacancies(self, data_to_add):
        pass


class JsonHandler(Handler):
    """Класс для сохранения информации о вакансиях в JSON-файл."""
    def __init__(self, filename):
        super().__init__(filename)
        self.__filename = filename

    def read_vacancies(self):
        """Читает вакансии из JSON-файла."""
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Если файла нет, возвращаем пустой список
        except json.JSONDecodeError:
            return []  # Если файл пустой или содержит невалидный JSON

    def add_vacancies(self, data_to_add):
        """Добавляет вакансии в JSON-файл."""
        data = self.read_vacancies()  # Читаем существующие вакансии

        if not data:  # Если файл пуст или не существует
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(data_to_add, file, ensure_ascii=False, indent=4)
            return

        # Обновляем существующие вакансии с новыми данными (если нужно)
        # Здесь логика зависит от того, как вы хотите обновлять данные.
        # Например, добавить новые вакансии к существующим:
        data.extend(data_to_add)

        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


# Пример использования:
if __name__ == '__main__':
    filename = 'vacancies.json'
    json_handler = JsonHandler(filename)

    new_vacancies = [
        {'id': 1, 'title': 'Python Developer', 'company': 'Google'},
        {'id': 2, 'title': 'Data Scientist', 'company': 'Microsoft'}
    ]

    json_handler.add_vacancies(new_vacancies)

    vacancies = json_handler.read_vacancies()
    print(vacancies)