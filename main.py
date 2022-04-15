import logging
import subprocess
import sys

import get
import gui
import filter
import search
from create_tables import engine, get_session, ProjectBasic, ProjectDetails
from config import settings


def main():
    # Connect logs
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    assert subprocess.call([sys.executable, 'create_tables.py']) == 0

    all_projects_response = get.all_projects()['data']
    all_projects = []

    for project in all_projects_response:
        all_projects.append(ProjectBasic(
            id=project['id'],
            number=project['number'],
            name=project['nameRus'],
            head=project['head'],
            workers=len(get.project_team(project['id'])),
            vacancies=project['vacancies'],
            status=project['statusDesc'],
            image=project['thumbnail']
        ))

    # project info
    link = get.project_link(0)
    basic_info_response = get.project_basic_info(0)['data']
    details_response = get.project_details(0)['data']
    vacancies_response = get.project_vacancies(0)['data']
    team_response = get.project_team(0)['data']

    project_info = ProjectDetails(
        id=basic_info_response['id'],
        number=basic_info_response['number'],
        name=basic_info_response['nameRus'],
        head=basic_info_response['mainLeader']['fio'],
        team=team_response['data'],
        vacancies=vacancies_response['data'],
        status=basic_info_response['statusLabel'],
        type=basic_info_response['typeLabel'],
        years=basic_info_response['years'],
        link=link,
        zulip_link=basic_info_response['chat'],
        wiki_link=basic_info_response['wiki'],
        email=basic_info_response['googleGroup'],
        image=basic_info_response['thumbnail'],
        target=details_response['target'],
        annotation=details_response['annotation'],
        competency=details_response['competency'],
        resource=details_response['resource'],
        control=details_response['control'],
        background=details_response['background'],
        result_form=details_response['result_form'],
        results=details_response['results'],
        organization=details_response['organization'],
        customer=details_response['customer'],
        industry=details_response['industry']
    )


if __name__ == '__main__':
    main()
