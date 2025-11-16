from typing import Any, Iterable, List, Optional

from bs4 import BeautifulSoup

from pythonproject11.src.vacancy import Vacancy


def clean_html_to_text(html_text: Optional[str]) -> str:
    """Очищает HTML в текст (с использованием BeautifulSoup)."""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def create_vacancy_objects(vacancies_data: Iterable[dict[str, Any]]) -> List[Vacancy]:
    """Создает список объектов Vacancy."""
    vacancies = []

    for data in vacancies_data:
        title = data.get("name", "")
        url = data.get("alternate_url", "")
        salary_data = data.get("salary")
        salary_from = salary_data.get("from") if salary_data else None
        salary_to = salary_data.get("to") if salary_data else None

        snippet = data.get("snippet")
        if snippet:
            requirement_html = snippet.get("requirement")
            responsibility_html = snippet.get("responsibility")

            requirement = clean_html_to_text(requirement_html) if requirement_html else ""
            responsibility = clean_html_to_text(responsibility_html) if responsibility_html else ""

            description = (
                f"Требования: {requirement}. Обязанности: {responsibility}" if requirement or responsibility else ""
            )
        else:
            description = ""

        vacancy = Vacancy(title, url, salary_from, salary_to, description)
        vacancies.append(vacancy)

    return vacancies
