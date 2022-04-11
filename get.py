import requests
import json

from config import settings


def all_projects() -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.BASE_URL}/projects'
    ).json()

    return response


def project_link(project_id: int) -> str:
    return f'https://cabinet.miem.hse.ru/#/project/{project_id}'


def project_details(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.BASE_URL}/project/body/{project_id}'
    ).json()

    return response


def project_vacancies(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.BASE_URL}/project/vacancies/{project_id}'
    )

    return response


def project_team(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.BASE_URL}/project/{project_id}/team'
    )

    return response


def userstories_stats() -> json:

    headers = {
        'content-type': 'application/json',
        'x-disable-pagination': 'true'
    }

    taiga_response = requests.get(
        'https://track.miem.hse.ru/api/v1/userstories?',
        headers=headers
    ).json()

    return taiga_response


def get_tasks_stats() -> json:

    headers = {
        'content-type': 'application/json',
        'x-disable-pagination': 'true'
    }

    taiga_response = requests.get(
        'https://track.miem.hse.ru/api/v1/tasks',
        headers=headers
    ).json()

    return taiga_response
