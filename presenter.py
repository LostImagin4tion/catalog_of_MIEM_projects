from typing import List
from sqlalchemy.orm import Session

from create_tables import ProjectBasic


def perform_searching(
        sort: str,
        status: str,
        type: str,
        vacancies: str,
        entry: str,
        session: Session
) -> List[ProjectBasic]:
    status_to_api_status = {
        'Все': None,
        'Готов к работе': 'Готов к работе',
        'Рабочий': 'Рабочий'
    }
    type_to_api_type = {
        'Все': None,
        'Программный': 'Прогр.',
        'Прогр.-аппаратный': 'Прогр-аппарат.',
        'НИР': 'НИР'
    }
    vacancies_to_int = {
        'Все': None,
        'Набор закрыт': 0,
        'Есть вакансии': 1
    }

    status_value = status_to_api_status[status]
    type_value = type_to_api_type[type]
    vacancies_value = vacancies_to_int[vacancies]
    entry = None \
        if entry == ' Введите номер, название или руководителя проекта'\
        else entry

    db_projects = session.query(ProjectBasic)
    filtered_projects = []
    search_result = []

    if status_value is None and type_value is None and vacancies_value is None:
        filtered_projects = db_projects
    else:
        if status_value is None and type_value is not None:
            db_projects = db_projects.filter_by(type=type_value)
        elif status_value is not None and type_value is None:
            db_projects = db_projects.filter_by(status=status_value)
        elif status_value is not None and type_value is not None:
            db_projects = db_projects.filter_by(status=status_value, type=type_value)

        if vacancies_value is None:
            filtered_projects = db_projects
        else:
            for project in db_projects:
                if vacancies_value == 'Набор закрыт' and project.vacancies == 0:
                    filtered_projects.append(project)
                elif vacancies_value == 'Есть вакансии' and project.vacancies > 0:
                    filtered_projects.append(project)

    if entry is None:
        search_result = filtered_projects
    else:
        for project in filtered_projects:
            if project.number == entry or project.name == entry or project.head == entry:
                search_result.append(project)

    return search_result
