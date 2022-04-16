import requests
import json

from config import settings


def all_projects() -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.PUBLIC_API}/projects'
    ).json()

    return response['data']


def project_link(project_id: int) -> str:
    return f'https://cabinet.miem.hse.ru/#/project/{project_id}'


def project_basic_info(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.PUBLIC_API}/project/header/{project_id}'
    ).json()

    return response['data']


def project_details(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.PUBLIC_API}/project/body/{project_id}'
    ).json()
    return response['data']


def project_vacancies(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.PUBLIC_API}/project/vacancies/{project_id}'
    ).json()

    return response['data']


def project_team(project_id: int) -> json:
    response = requests.get(
        f'{settings.BASE_URL}/{settings.PUBLIC_API}/project/{project_id}/team'
    ).json()

    return response['data']