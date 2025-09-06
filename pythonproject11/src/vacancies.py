class Vacancy:
    def __init__(self, title, url, salary_from, salary_to, description):
        self.title = title
        self.url = url
        self.description = description

        if salary_from is not None and salary_to is not None:
            self._avg_salary = (salary_from + salary_to) / 2
        elif salary_from is not None:
            self._avg_salary = salary_from
        elif salary_to is not None:
            self._avg_salary = salary_to
        else:
            self._avg_salary = 0  # Или None, если хотите

    @property
    def salary(self):
        return self._avg_salary

    @salary.setter
    def salary(self, avg_salary):
        if isinstance(avg_salary, (int, float)):
            self._avg_salary = avg_salary
        else:
            self._avg_salary = 0

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        raise ValueError('Невозможно сравнить: два разных типа.')

    def __str__(self):
        return f'Название: {self.title}, зарплата: {self.salary}.'

    def cast_to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description
        }

if __name__ == '__main__':
    v = Vacancy('название', 'lflsk', 8, 6, 'yj;ybw')
    v1 = Vacancy('название', 'lf', 10, 20, 'ножницы')
    _list = [v, v1]
    [print(v) for v in sorted(_list, reverse=True)]