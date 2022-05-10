import functools
from typing import List
import win32api
import webbrowser
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from sqlalchemy.orm import Session
from random import randint

import scripts.create_tables
from scripts.create_tables import ProjectBasic, ProjectDetails
import scripts.get
import scripts.export
import scripts.presenter


class App:
    def __init__(self, root: Tk, session: Session):
        self.session = session
        self.all_projects = []
        self.all_details = []

        self.root = root
        self.root.title('Каталог проектов')

        self.projects_list = Listbox(selectmode=EXTENDED, height=36, width=101)
        self.projects_list.place(x=20, y=110)
        self.projects_list.bind('<<ListboxSelect>>', self.__on_click_projects_list)

        self.project_scroll_vertical = Scrollbar(self.root, orient='vertical', command=self.projects_list.yview)
        self.project_scroll_horizontal = Scrollbar(self.root, orient='horizontal', command=self.projects_list.xview)
        self.project_scroll_horizontal.place(x=22, y=690, width=605)
        self.project_scroll_vertical.place(x=630, y=110, height=582)

        self.projects_list.config(
            xscrollcommand=self.project_scroll_horizontal.set,
            yscrollcommand=self.project_scroll_vertical.set
        )

        self.find_field = Entry(root, width=65)
        self.find_field.insert(0, ' Введите номер, название или руководителя проекта')
        self.find_field.place(x=65, y=15)
        self.find_field.bind('<FocusIn>', lambda args: self.find_field.delete(0, END))

        self.search_img = PhotoImage(file='drawables/ic_search.png', width=16, height=16)
        self.search_button = Button(root, image=self.search_img, command=functools.partial(self.__search))
        self.search_button.place(x=480, y=12)

        self.update_img = PhotoImage(file='drawables/ic_update.png', width=16, height=16)
        self.update_button = Button(root, image=self.update_img, command=functools.partial(self.__update))
        self.update_button.place(x=515, y=12)

        self.export_img = PhotoImage(file='drawables/ic_export.png', width=16, height=16)
        self.export_button = Button(root, image=self.export_img, command=functools.partial(self.__export))
        self.export_button.place(x=550, y=12)

        # project status filters
        self.filter_top = Label(root, text='Cтатус:')
        self.filter_top.place(x=135, y=50)

        self.project_status_filters = Combobox(
            root,
            values=[
                'Все',
                'Готов к работе',
                'Рабочий'],
            state='readonly'
        )
        self.project_status_filters.place(x=85, y=70)
        self.project_status_filters.current(0)

        # project type filters
        self.filter_top = Label(root, text='Тип:')
        self.filter_top.place(x=295, y=50)
        self.project_type_filters = Combobox(
            root,
            values=[
                'Все',
                'НИР',
                'Программный',
                'Прогр.-аппаратный',
                'Стартап'],
            state='readonly'
        )
        self.project_type_filters.place(x=238, y=70)
        self.project_type_filters.current(0)

        # project vacancies filters
        self.filter_top = Label(root, text='По наличию вакансий:')
        self.filter_top.place(x=395, y=50)
        self.project_vacancies_filters = Combobox(
            root,
            values=[
                'Все',
                'Есть вакансии',
                'Набор закрыт'],
            state='readonly'
        )
        self.project_vacancies_filters.place(x=390, y=70)
        self.project_vacancies_filters.current(0)

        # setup projects list
        self.__setup_projects()

    def __search(self) -> None:
        self.all_projects = scripts.presenter.perform_searching(
            self.project_status_filters.get(),
            self.project_type_filters.get(),
            self.project_vacancies_filters.get(),
            self.find_field.get(),
            self.session
        )
        self.__update(self.all_projects)

    def __open_link(self, link: str) -> None:
        webbrowser.open(url=link, new=0, autoraise=True)

    def __mail(self, link: str) -> None:
        win32api.ShellExecute(0, 'open', f'mailto:{link}', None, None, 0)

    def __update(self, new_projects: List[ProjectBasic] = None) -> None:
        self.projects_list.delete(0, END)

        if new_projects is None:
            scripts.create_tables.truncate_tables()
            self.all_projects = []
            self.__setup_projects()
        else:
            if not isinstance(new_projects, list):
                new_projects = new_projects[0]
            self.all_projects = new_projects
            self.__setup_projects(new_projects)

    def __export(self) -> None:
        scripts.export.to_excel(self.all_projects)

    def __setup_projects(self, new_projects: List[ProjectBasic] = None) -> int:

        if new_projects is not None:
            for project in new_projects:
                project_number = project.number if project.number else project.id
                project_label = f'#{project_number}    {project.name}    ({project.head})'
                self.projects_list.insert(END, project_label)
        else:
            project_query = self.session.query(ProjectBasic)

            if project_query.count():
                for project in self.session.query(ProjectBasic):
                    self.all_projects.append(ProjectBasic(
                        id=project.id,
                        number=project.number,
                        name=project.name,
                        head=project.head,
                        vacancies=project.vacancies,
                        status=project.status,
                        type=project.type,
                        image=project.image,
                    ))

                    project_number = project.number if project.number else project.id
                    project_label = f'#{project_number}    {project.name}    ({project.head})'
                    self.projects_list.insert(END, project_label)
            else:
                projects_response = scripts.get.all_projects()

                for project in projects_response:
                    project_info = ProjectBasic(
                        id=project['id'],
                        number=project['number'],
                        name=project['nameRus'],
                        head=project['head'],
                        vacancies=project['vacancies'],
                        status=project['statusDesc'],
                        type=project['typeDesc'],
                        image=project['thumbnail']
                    )
                    self.all_projects.append(project_info)

                    project_number = project_info.number if project_info.number else project_info.id
                    project_label = f'#{project_number}    {project_info.name}    ({project_info.head})'
                    self.projects_list.insert(END, project_label)

                    project_entry = ProjectBasic(
                        id=project_info.id,
                        number=project_info.number,
                        name=project_info.name,
                        head=project_info.head,
                        vacancies=project_info.vacancies,
                        status=project_info.status,
                        type=project_info.type,
                        image=project_info.image,
                    )
                    self.session.add(project_entry)

            self.session.commit()

        return 0

    def __on_click_projects_list(self, event) -> None:

        self.selected_item = self.projects_list.curselection()
        if not isinstance(self.all_projects, list):
            self.all_projects = self.all_projects[0]

        project_id = self.all_projects[self.selected_item[0]].id

        if project_id is not None and isinstance(project_id, int):
            project_info = self.session.query(ProjectBasic).filter_by(id=project_id).first()

            if project_info:
                self.project_card = Toplevel(self.root)
                self.project_card.geometry('450x700')
                self.project_card.title('Карточка проекта')

                index = randint(1, 4)
                self.img = PhotoImage(file=f'drawables/example{index}.png')
                self.thumbnail = Label(self.project_card, image=self.img)
                self.thumbnail.place(x=-5, y=0, width=455, height=100)

                project_number = f'#{project_info.number}' if project_info.number else '-'
                self.project_number = Label(self.project_card, text=project_number, font='Times 15')
                self.project_number.place(x=225, y=125, anchor=CENTER)

                self.project_name = Message(
                    self.project_card,
                    text=f'{project_info.name}',
                    font='Times 15',
                    aspect=300,
                )
                self.project_name.configure(justify='center')
                self.project_name.place(x=35, y=140, width=390)

                self.vacancies_number = Label(
                    self.project_card,
                    text=f' {project_info.vacancies} свободных вакансий ',
                    borderwidth=2,
                    relief="groove",
                    font='Times 13'
                )
                self.vacancies_number.place(x=225, y=300, anchor=CENTER)

                self.project_status = Label(
                    self.project_card,
                    text=f' {project_info.status} ',
                    borderwidth=2,
                    relief='groove',
                    font='Times 13'
                )
                self.project_status.place(x=225, y=330, anchor=CENTER)

                self.project_head_title = Label(
                    self.project_card,
                    text=f'Руководитель:',
                    font='Times 13'
                )
                self.project_head_title.place(x=225, y=380, anchor=CENTER)

                self.project_head_name = Label(self.project_card, text=project_info.head, font='Times 13')
                self.project_head_name.place(x=225, y=405, anchor=CENTER)

                self.project_type_title = Label(self.project_card, text=f'Тип: {project_info.type}', font='Times 13')
                self.project_type_title.place(x=225, y=460, anchor=CENTER)

                self.about_button = Button(
                    self.project_card,
                    text='Подробнее',
                    command=functools.partial(self.__about_project, project_id)
                )
                self.about_button.place(x=225, y=550, relheight=.1, relwidth=.4, anchor=CENTER)

                self.back = Button(
                    self.project_card,
                    text='Закрыть',
                    command=self.project_card.destroy
                )
                self.back.place(x=135, y=600, relheight=.1, relwidth=.4)

    def __about_project(self, project_id: int) -> None:

        if project_id:
            project_basic_info = self.session.query(ProjectBasic).filter_by(id=project_id).first()
            project_full_info = self.session.query(ProjectDetails).filter_by(id=project_id).first()

            if not project_full_info:
                project_details = scripts.get.project_details(project_id)
                project_team = scripts.get.project_team(project_id)
                project_vacancies = scripts.get.project_vacancies(project_id)
                project_links = scripts.get.project_basic_info(project_id)

                project_full_info = ProjectDetails(
                    id=project_basic_info.id,
                    name=project_basic_info.name,
                    team=project_team,
                    vacancies=project_vacancies,
                    link=scripts.get.project_link(project_basic_info.id),
                    wiki_link=project_links['wiki'],
                    zulip_link=project_links['chat'],
                    email=project_links['googleGroup'],
                    target=project_details['target'],
                    annotation=project_details['annotation'],
                    results=project_details['results'],
                    competency=project_details['competency'],
                    resources=project_details['resource'],
                    control=project_details['control'],
                    result_form=project_details['resultForm'],
                    background=project_details['background'],
                    customer=project_details['projectClientLabel'],
                    industry=project_details['projectIndustryLabel'] if 'projectIndustryLabel'
                                                                        in project_details.keys() else None,
                    organization=project_details['organization']
                )

            self.about_window = Toplevel(self.project_card)
            self.about_window.geometry('500x800')
            self.about_window.title('Подробнее')

            self.email_img = ImageTk.PhotoImage(Image.open('drawables/ic_email.png'), width=24, height=24)
            self.email_button = Button(
                self.about_window,
                image=self.email_img,
                command=functools.partial(self.__mail, project_full_info.email)
            )
            self.email_button.place(x=370, y=10)

            self.wiki_img = ImageTk.PhotoImage(Image.open('drawables/ic_wiki.png'), width=24, height=24)
            self.wiki_button = Button(
                self.about_window,
                image=self.wiki_img,
                command=functools.partial(self.__open_link, project_full_info.wiki_link)
            )
            self.wiki_button.place(x=410, y=10)

            self.zulip_img = ImageTk.PhotoImage(Image.open('drawables/ic_zulip.png'), width=24, height=24)
            self.zulip_button = Button(
                self.about_window,
                image=self.zulip_img,
                command=functools.partial(self.__open_link, project_full_info.zulip_link)
            )
            self.zulip_button.place(x=450, y=10)

            self.cabinet_button = Button(
                self.about_window,
                text='Посмотреть на сайте',
                command=functools.partial(self.__open_link, project_full_info.link)
            )
            self.cabinet_button.place(x=364, y=50)

            self.back = Button(self.about_window, text='Закрыть', command=self.about_window.destroy)
            self.back.place(x=390, y=80)

            self.project_number = Label(self.about_window, text=f'Проект #{project_basic_info.number},'
                                                                f' {project_basic_info.type}', font='Times 13')
            self.project_number.place(x=10, y=10)

            self.project_type = Label(self.about_window, text=f'{project_basic_info.status}', font='Times 13')
            self.project_type.place(x=10, y=30, width=200)

            self.project_name = Message(
                self.about_window,
                text=f'{project_basic_info.name}',
                font='Times 13',
                anchor='nw',
                aspect=300
            )
            self.project_name.place(x=5, y=50, width=360)

            self.notebook = Notebook(self.about_window)
            self.notebook.place(x=10, y=160)

            # Frames
            self.first_frame = Frame(self.notebook, width=470, height=610)
            self.second_frame = Frame(self.notebook, width=470, height=610)
            self.third_frame = Frame(self.notebook, width=470, height=610)
            self.notebook.add(self.first_frame, text='Общая информация')
            self.notebook.add(self.second_frame, text='Вакансии')
            self.notebook.add(self.third_frame, text='Команда')

            # FRAME 1
            # помещение текста в первое окно + перенос строк

            target = project_full_info.target if project_full_info.target else 'Не указано'
            annotation = project_full_info.annotation if project_full_info.annotation else 'Не указано'
            results = project_full_info.results if project_full_info.results else 'Не указано'
            competency = project_full_info.competency if project_full_info.competency else 'Не указано'
            resources = project_full_info.resources if project_full_info.resources else 'Не указано'
            control = project_full_info.control if project_full_info.control else 'Не указано'
            result_form = project_full_info.result_form if project_full_info.result_form else 'Не указано'
            background = project_full_info.background if project_full_info.background else 'Не указано'
            customer = project_full_info.customer if project_full_info.customer else 'Не указано'
            industry = project_full_info.industry if project_full_info.industry else 'Не указано'
            organization = project_full_info.organization if project_full_info.organization else 'Не указано'

            text_info = f'Цель проекта:\n{target}\n\n' \
                        f'Краткая аннотация проекта (общая информация о проекте):\n{annotation}\n\n' \
                        f'Ожидаемые результаты:\n{results}\n\n' \
                        f'Требуемые и приобретаемые навыки:\n{competency}\n\n' \
                        f'Ресурсное обеспечение:\n{resources}\n\n' \
                        f'Форма и способы промежуточного контроля:\n{control}\n\n' \
                        f'Форма представления результатов:\n{result_form}\n\n' \
                        f'Имеющийся задел:\n{background}\n' \
                        f'Заказчик проекта:\n{customer}\n\n' \
                        f'Отрасль проекта:\n{industry}\n\n' \
                        f'Если проект в интересах организации или подразделения ВУЗа, пожалуйста, укажите название' \
                        f'\n{organization}\n'

            self.text_info_widget = Text(self.first_frame, width=56, height=33)
            self.text_info_widget.place(x=0, y=0)
            self.text_info_widget.config(
                foreground="black",
                font='times 12 ',
                wrap='word'
            )
            self.text_info_widget.insert(END, text_info)

            self.text_info_scroll = Scrollbar(
                self.first_frame,
                command=self.text_info_widget.yview,
                orient=VERTICAL
            )
            self.text_info_scroll.place(x=453, y=0, height=620)
            self.text_info_widget.config(yscrollcommand=self.text_info_scroll.set)

            # FRAME 2
            # помещение текста в первое окно + перенос строк

            text_vacancies = ''
            for vacancy in project_full_info.vacancies:
                text_vacancies += f'{vacancy["role"]}' \
                                  f'\n\n   Обязательно знать/уметь:'

                for discipline in vacancy['disciplines']:
                    text_vacancies += f'\n     {discipline}'

                text_vacancies += '\n\n  Желательно знать/уметь:'

                for recommendation in vacancy['additionally']:
                    text_vacancies += f'\n     {recommendation}'

                text_vacancies += '\n\n'

            self.text_vacancies_widget = Text(self.second_frame, width=56, height=33)
            self.text_vacancies_widget.place(x=0, y=0)
            self.text_vacancies_widget.config(
                foreground='black',
                font='times 12 ',
                wrap='word')
            self.text_vacancies_widget.insert(END, text_vacancies)

            self.text_vacancies_scroll = Scrollbar(
                self.second_frame,
                command=self.text_vacancies_widget.yview,
                orient=VERTICAL
            )
            self.text_vacancies_scroll.place(x=453, y=0, height=620)
            self.text_vacancies_widget.config(yscrollcommand=self.text_vacancies_scroll.set)

            # FRAME 3
            # помещение текста в первое окно + перенос строк

            text_team = ''
            for teammate in project_full_info.team:
                text_team += f'{teammate["name"]} ({teammate["position"]})\n'

            self.text_team_widget = Text(self.third_frame, width=56, height=33)
            self.text_team_widget.place(x=0, y=0)
            self.text_team_widget.config(
                foreground='black',
                font='times 12 ',
                wrap='word')
            self.text_team_widget.insert(END, text_team)

            self.text_team_scroll = Scrollbar(
                self.third_frame,
                command=self.text_team_widget.yview,
                orient=VERTICAL
            )
            self.text_team_scroll.place(x=453, y=0, height=620)
            self.text_team_widget.config(yscrollcommand=self.text_team_scroll.set)
