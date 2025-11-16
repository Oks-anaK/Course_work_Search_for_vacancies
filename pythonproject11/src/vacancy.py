from typing import Any, Optional, Union


class Vacancy:
    """Класс для работы с вакансиями, поддерживает методы сравнения
    вакансий между собой по зарплате и валидирует данные."""

    __slots__ = ["title", "url", "description", "_avg_salary"]

    # Аннотации атрибутов (PEP 526)
    title: str
    url: str
    description: str
    _avg_salary: float

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Optional[Union[int, float]],
        salary_to: Optional[Union[int, float]],
        description: str,
    ) -> None:
        """Функция инициализации атрибутов."""
        self.title = title
        self.url = url
        self.description = description
        self._avg_salary = self.__validate_salary(salary_from, salary_to)

    def __validate_salary(
        self, salary_from: Optional[Union[int, float]], salary_to: Optional[Union[int, float]]
    ) -> float:
        """Функция валидации данных."""
        if salary_from is not None and salary_to is not None:
            if not (isinstance(salary_from, (int, float)) and isinstance(salary_to, (int, float))):
                raise ValueError("Зарплата должна быть числом")
            return (salary_from + salary_to) / 2
        elif salary_from is not None:
            if not isinstance(salary_from, (int, float)):
                raise ValueError("Зарплата должна быть числом")
            return float(salary_from)
        elif salary_to is not None:
            if not isinstance(salary_to, (int, float)):
                raise ValueError("Зарплата должна быть числом")
            return float(salary_to)
        else:
            return 0.0

    @property
    def salary(self) -> float:
        """Геттер средней зарплаты."""
        return self._avg_salary

    @salary.setter
    def salary(self, avg_salary: Union[int, float]) -> None:
        """Сеттер для изменения средней зарплаты."""
        if isinstance(avg_salary, (int, float)):
            self._avg_salary = float(avg_salary)
        else:
            self._avg_salary = 0.0

    def __lt__(self, other: object) -> bool:
        """Метод сравнения зарплаты (меньше)."""
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        raise ValueError("Невозможно сравнить: два разных типа.")

    def __le__(self, other: object) -> bool:
        """Метод сравнения зарплаты (меньше или равно)."""
        if isinstance(other, Vacancy):
            return self.salary <= other.salary
        raise ValueError("Невозможно сравнить: два разных типа.")

    def __eq__(self, other: object) -> bool:
        """Метод сравнения зарплаты (равно)."""
        if isinstance(other, Vacancy):
            return self.salary == other.salary
        return False

    def __gt__(self, other: object) -> bool:
        """Метод сравнения зарплаты (больше)."""
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        raise ValueError("Невозможно сравнить: два разных типа.")

    def __ge__(self, other: object) -> bool:
        """Метод сравнения зарплаты (больше или равно)."""
        if isinstance(other, Vacancy):
            return self.salary >= other.salary
        raise ValueError("Невозможно сравнить: два разных типа.")

    def __str__(self) -> str:
        """Строковое представление вывода."""
        return f"Название: {self.title}, зарплата: {self.salary}."

    def cast_to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title or "",
            "url": self.url or "",
            "salary": self.salary,
            "description": self.description or "",
        }

    def __repr__(self) -> str:
        """Представление отладочной информации."""
        return f"Vacancy(title='{self.title}', salary={self.salary})"


# if __name__ == "__main__":
#     v = Vacancy("название", "lflsk", 8, 6, "yj;ybw")
#     v1 = Vacancy("название", "lf", 10, 20, "ножницы")
#     _list = [v, v1]
#     [print(v) for v in sorted(_list, reverse=True)]
