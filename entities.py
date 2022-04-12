from typing import Optional, List, Dict


class ProjectBasic:
    def __init__(
            self,
            id: Optional[int],
            name: Optional[str],
            head: Optional[str],
            status: Optional[str],
            workers: Optional[int] = None,
            vacancies: Optional[int] = None,
            number: Optional[int] = None,
            image: Optional[str] = None
    ):
        self.id = id
        self.number = number
        self.name = name
        self.head = head
        self.workers_number = workers
        self.vacancies = vacancies,
        self.status = status
        self.image = image


class ProjectDetails:
    def __init__(
            self,
            id: Optional[str],
            name: Optional[str],
            head: Optional[str],
            team: Optional[List[Dict[str, str]]],
            vacancies: Optional[List[Dict[str, str]]],
            status: Optional[str],
            type: Optional[List[str]],
            years: Optional[List[str]],
            link: Optional[str],
            zulip_link: Optional[str] = None,
            wiki_link: Optional[str] = None,
            email: Optional[str] = None,
            image: Optional[str] = None,
            target: Optional[str] = None,
            annotation: Optional[str] = None,
            competency: Optional[str] = None,
            resource: Optional[str] = None,
            control: Optional[str] = None,
            background: Optional[str] = None,
            result_form: Optional[str] = None,
            results: Optional[str] = None,
            organization: Optional[str] = None,
            customer: Optional[str] = None,
            industry: Optional[str] = None,
            number: Optional[str] = None,
    ):
        self.id = id
        self.number = number
        self.name = name
        self.head = head
        self.team = team
        self.vacancies = vacancies
        self.status = status
        self.type = type
        self.years = years
        self.image = image
        self.link = link
        self.zulip = zulip_link
        self.wiki = wiki_link
        self.email = email
        self.target = target
        self.annotation = annotation
        self.results = results
        self.competency = competency
        self.resources = resource
        self.control = control
        self.result_form = result_form
        self.background = background
        self.customer = customer
        self.industry = industry
        self.organization = organization
