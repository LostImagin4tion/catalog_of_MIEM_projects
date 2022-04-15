from typing import List, Dict
from sqlalchemy.orm import Session
import xlsxwriter

from create_tables import ProjectBasic, ProjectDetails


def to_excel(
        project_list: List[ProjectBasic],
        session: Session
) -> None:

    workbook = xlsxwriter.Workbook('Отчёт о проектах МИЭМа.xlsx')
    basic_info_worksheet = workbook.add_worksheet('Базовая информация')

    header_cell_format = workbook.add_format(
        {
            'bold': True,
            'text_wrap': True,
            'border': True,
            'valign': 'top',
            'font_name': 'Times New Roman',
            'font_size': '14',
            'bg_color': '#77bf77'
        }
    )
    default_cell_format = workbook.add_format(
        {
            'text_wrap': True,
            'border': True,
            'valign': 'top',
            'font_name': 'Times New Roman',
            'font_size': '12'
        }
    )

    basic_col = 0
    basic_row = 1

    basic_info_worksheet.write(0, basic_col, 'ID', header_cell_format)
    basic_info_worksheet.write(0, basic_col+1, 'Номер', header_cell_format)
    basic_info_worksheet.write(0, basic_col+2, 'Название', header_cell_format)
    basic_info_worksheet.write(0, basic_col+3, 'Руководитель', header_cell_format)
    basic_info_worksheet.write(0, basic_col+4, 'Кол-во вакансий', header_cell_format)
    basic_info_worksheet.write(0, basic_col+5, 'Статус', header_cell_format)
    basic_info_worksheet.write(0, basic_col+6, 'Тип', header_cell_format)
    basic_info_worksheet.write(0, basic_col+7, 'Ссылка на обложку', header_cell_format)

    for project in project_list:

        basic_info_worksheet.write(basic_row, basic_col, project.id, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+1, project.number, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+2, project.name, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+3, project.head, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+4, project.vacancies, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+5, project.vacancies, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+6, project.type, default_cell_format)
        basic_info_worksheet.write(basic_row, basic_col+7, project.image, default_cell_format)

        basic_row += 1

    workbook.close()
