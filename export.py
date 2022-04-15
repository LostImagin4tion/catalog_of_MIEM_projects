from typing import List, Dict
from sqlalchemy.orm import Session
import xlsxwriter
import json

from create_tables import ProjectBasic, ProjectDetails
import get


def to_excel(
        project_list: List[ProjectBasic],
        session: Session
) -> None:

    workbook = xlsxwriter.Workbook('Отчёт о проектах МИЭМа.xlsx')
    basic_info_worksheet = workbook.add_worksheet('Базовая информация')
    details_worksheet = workbook.add_worksheet('Подробная информация')

    header_cell_format = workbook.add_format(
        {
            'bold': True,
            'text_wrap': True,
            'border': True,
            'font_name': 'Times New Roman',
            'font_size': '14',
            'bg_color': '#77bf77'
        }
    )
    default_cell_format = workbook.add_format(
        {
            'text_wrap': True,
            'border': True,
            'font_name': 'Times New Roman',
            'font_size': '12'
        }
    )

    basic_col = 0
    basic_row = 1
    details_col = 0
    details_row = 1

    basic_info_worksheet.write(0, basic_col, 'ID', header_cell_format)
    basic_info_worksheet.write(0, basic_col+1, 'Номер', header_cell_format)
    basic_info_worksheet.write(0, basic_col+2, 'Название', header_cell_format)
    basic_info_worksheet.write(0, basic_col+3, 'Руководитель', header_cell_format)
    basic_info_worksheet.write(0, basic_col+4, 'Кол-во вакансий', header_cell_format)
    basic_info_worksheet.write(0, basic_col+5, 'Статус', header_cell_format)
    basic_info_worksheet.write(0, basic_col+6, 'Тип', header_cell_format)
    basic_info_worksheet.write(0, basic_col+7, 'Ссылка на обложку', header_cell_format)

    details_worksheet.write(0, details_col, 'ID', header_cell_format)
    details_worksheet.write(0, details_col+1, 'Номер', header_cell_format)
    details_worksheet.write(0, details_col+2, 'Название', header_cell_format)
    details_worksheet.write(0, details_col+3, 'Команда', header_cell_format)
    details_worksheet.write(0, details_col+4, 'Вакансии', header_cell_format)
    details_worksheet.write(0, details_col+5, 'Ссылка', header_cell_format)
    details_worksheet.write(0, details_col+6, 'Ссылка на вики', header_cell_format)
    details_worksheet.write(0, details_col+7, 'Ссылка на чат в зулипе', header_cell_format)
    details_worksheet.write(0, details_col+8, 'Почта', header_cell_format)
    details_worksheet.write(0, details_col+9, 'Цель проекта', header_cell_format)
    details_worksheet.write(0, details_col+10, 'Аннотация', header_cell_format)
    details_worksheet.write(0, details_col+11, 'Предполагаемые результаты', header_cell_format)
    details_worksheet.write(0, details_col+12, 'Навыки', header_cell_format)
    details_worksheet.write(0, details_col+13, 'Ресурсы', header_cell_format)
    details_worksheet.write(0, details_col+14, 'Формы контроля', header_cell_format)
    details_worksheet.write(0, details_col+15, 'Форма представления результатов', header_cell_format)
    details_worksheet.write(0, details_col+16, 'Имеющийся задел', header_cell_format)
    details_worksheet.write(0, details_col+17, 'Заказчик проекта', header_cell_format)
    details_worksheet.write(0, details_col+18, 'Отрасль проекта', header_cell_format)
    details_worksheet.write(0, details_col+19, 'Организация', header_cell_format)

    for project in project_list:
        details = session.query(ProjectDetails).filter_by(id=project.id).first()

        basic_info_worksheet.write(basic_row, basic_col, project.id, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+1, project.number, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+2, project.name, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+3, project.head, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+4, project.vacancies, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+5, project.vacancies, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+6, project.type, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+7, project.image, default_cell_format)

        if details is not None:
            details_worksheet.write(details_row, details_col, details.id, default_cell_format)
            details_worksheet.write(details_row, details_col+1, project.number, default_cell_format)
            details_worksheet.write(details_row, details_col+2, details.name, default_cell_format)
            details_worksheet.write(details_row, details_col+3, details.team, default_cell_format)
            details_worksheet.write(details_row, details_col+4, details.vacancies, default_cell_format)
            details_worksheet.write(details_row, details_col+5, details.link, default_cell_format)
            details_worksheet.write(details_row, details_col+6, details.wiki_link, default_cell_format)
            details_worksheet.write(details_row, details_col+7, details.zulip_link, default_cell_format)
            details_worksheet.write(details_row, details_col+8, details.email, default_cell_format)
            details_worksheet.write(details_row, details_col+9, details.target, default_cell_format)
            details_worksheet.write(details_row, details_col+10, details.annotation, default_cell_format)
            details_worksheet.write(details_row, details_col+11, details.results, default_cell_format)
            details_worksheet.write(details_row, details_col+12, details.competency, default_cell_format)
            details_worksheet.write(details_row, details_col+13, details.resources, default_cell_format)
            details_worksheet.write(details_row, details_col+14, details.control, default_cell_format)
            details_worksheet.write(details_row, details_col+15, details.result_form, default_cell_format)
            details_worksheet.write(details_row, details_col+16, details.background, default_cell_format)
            details_worksheet.write(details_row, details_col+17, details.customer, default_cell_format)
            details_worksheet.write(details_row, details_col+18, details.industry, default_cell_format)
            details_worksheet.write(details_row, details_col+19, details.organization, default_cell_format)
        # else:
        #     details = get.project_details(project.id)
        #     team = get.project_team(project.id)
        #     vacancies = get.project_vacancies(project.id)
        #     links = get.project_basic_info(project.id)
        #
        #     details_worksheet.write(details_row, details_col, project.id, default_cell_format)
        #     details_worksheet.write(details_row, details_col + 1, project.number, default_cell_format)
        #     details_worksheet.write(details_row, details_col + 2, project.name, default_cell_format)
        #     details_worksheet.write(details_row, details_col + 3, json.dumps(team), default_cell_format)
        #     details_worksheet.write(details_row, details_col + 4, json.dumps(vacancies), default_cell_format)
        #     details_worksheet.write(details_row, details_col + 5, get.project_link(project.id), default_cell_format)
        #     details_worksheet.write(details_row, details_col + 6, links['wiki'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 7, links['chat'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 8, links['googleGroup'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 9, details['target'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 10, details['annotation'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 11, details['results'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 12, details['competency'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 13, details['resource'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 14, details['control'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 15, details['resultForm'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 16, details['background'], default_cell_format)
        #     details_worksheet.write(details_row, details_col + 17, details['projectClientLabel'], default_cell_format)
        #     details_worksheet.write(
        #         details_row,
        #         details_col + 18,
        #         details['projectIndustryLabel'] if 'projectIndustryLabel' in details.keys() else '', default_cell_format
        #     )
        #     details_worksheet.write(details_row, details_col + 19, details['organization'], default_cell_format)

        basic_row += 1
        details_row += 1

    workbook.close()
