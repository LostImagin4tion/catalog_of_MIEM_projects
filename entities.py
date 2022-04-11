from typing import Optional, List


class ProjectBasic:
    def __init__(
            self,
            id: Optional[int],
            head: Optional[str],
            workers: Optional[str],
            vacancies: Optional[int],
            status: Optional[str],
            number: Optional[int] = None,
            image: Optional[str] = None
    ):
        self.id = id
        self.number = number
        self.head = head
        self.workers_amount = workers
        self.vacancies = vacancies,
        self.status = status
        self.image = image


class ProjectDetails:
    def __init__(
            self,
            id: Optional[str],
            name: Optional[str],
            head: Optional[str],
            team: Optional[List[str]],
            vacancies: Optional[List[str]],
            status: Optional[str],
            years: Optional[List[str]],
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
        self.years = years
        self.image = image
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
