import json
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from sqlalchemy import desc
from sqlalchemy.orm import Session

import entities
from create_tables import engine, get_session, ProjectBasic, ProjectDetails
import get


class App:
    def __init__(
            self,
            root: Tk,
            session: Session
    ):
        self.session = session
        self.all_projects = []

        self.root = root
        self.root.title('Каталог проектов')

        self.projects_list = Listbox(selectmode=EXTENDED, height=35, width=102)

        self.projects_list.place(x=20, y=110)

        self.project_scroll_vertical = Scrollbar(command=self.projects_list.yview)
        self.project_scroll_vertical.place(x=617.4, y=112, height=560.25)

        self.project_scroll_horizontal = Scrollbar(command=self.projects_list.xview, orient='horizontal')
        self.project_scroll_horizontal.place(x=22, y=655, width=595)

        self.projects_list.config(
            xscrollcommand=self.project_scroll_horizontal.set,
            yscrollcommand=self.project_scroll_vertical.set
        )

        self.projects_list.bind('<<ListboxSelect>>')

        # self.canvas = Canvas(self.root, width=400, height=400)

        self.find_field = Entry(root, width=65)
        self.find_field.insert(0, ' Введите номер, название или руководителя проекта')
        self.find_field.place(x=65, y=15)

        self.search_img = PhotoImage(file='drawables/ic_search.png', width=16, height=16)
        self.search_button = Button(root, image=self.search_img, command=self.__search())
        self.search_button.place(x=480, y=12)

        self.update_img = PhotoImage(file='drawables/ic_update.png', width=16, height=16)
        self.update_button = Button(root, image=self.update_img, command=self.__update())
        self.update_button.place(x=515, y=12)

        self.export_img = PhotoImage(file='drawables/ic_export.png', width=16, height=16)
        self.export_button = Button(root, image=self.export_img, command=self.__export())
        self.export_button.place(x=550, y=12)

        # sorting
        self.sort_top = Label(root, text='Сортировать:')
        self.sort_top.place(x=48, y=50)

        self.sort_value = Combobox(root, values=[
            'По названию А-Я',
            'По названию Я-А',
            'По номеру 0-...',
            'По номеру ...-0',
            'По руководителю А-Я',
            'По руководителю Я-А'
        ])
        self.sort_value.place(x=20, y=70)
        self.sort_value.current(0)

        # project status filters
        self.filter_top = Label(root, text='Cтатус:')
        self.filter_top.place(x=235, y=50)

        self.project_status_filters = Combobox(root, values=[
            'Все',
            'Готов к работе',
            'Рабочий'
        ])
        self.project_status_filters.place(x=185, y=70)
        self.project_status_filters.current(0)

        # project type filters
        self.filter_top = Label(root, text='Тип:')
        self.filter_top.place(x=395, y=50)
        self.project_type_filters = Combobox(root, values=[
            'Все',
            'НИР',
            'Программный',
            'Прогр.-аппаратный',
            'Стартап'
        ])
        self.project_type_filters.place(x=338, y=70)
        self.project_type_filters.current(0)

        # project vacancies filters
        self.filter_top = Label(root, text='По наличию вакансий:')
        self.filter_top.place(x=495, y=50)
        self.project_vacancies_filters = Combobox(root, values=[
            'Все',
            'Есть вакансии',
            'Набор закрыт'
        ])
        self.project_vacancies_filters.place(x=490, y=70)
        self.project_vacancies_filters.current(0)

        # setup projects list
        self.__setup_projects()

    def __search(self):
        return 0

    def __wiki(self):
        return 0

    def __update(self):
        return 0

    def __export(self):
        return 0

    def __setup_projects(self):

        project_query = self.session.query(ProjectBasic)

        if project_query.count():
            for project in self.session.query(ProjectBasic):

                self.all_projects.append(entities.ProjectBasic(
                    id=project.id,
                    number=project.number,
                    name=project.name,
                    head=project.head,
                    vacancies=project.vacancies,
                    status=project.status,
                    workers=project.team,
                    image=project.image
                ))

                project_number = project.number if project.number else project.id
                project_info = f'#{project_number}    {project.name}    ({project.head})'
                self.projects_list.insert(END, project_info)
        else:
            projects_response = get.all_projects()

            for project in projects_response:

                project_info = entities.ProjectBasic(
                    id=project['id'],
                    number=project['number'],
                    name=project['nameRus'],
                    head=project['head'],
                    vacancies=project['vacancies'],
                    status=project['statusDesc'],
                    workers=len(get.project_team(project['id'])),
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
                    workers_amount=project_info.workers_number,
                    vacancies=project_info.vacancies,
                    status=project_info.status,
                    image=project_info.image
                )
                self.session.add(project_entry)

        self.session.commit()

        return 0

    def __on_click_projects_list(self, project_id):

        self.card_title = Label(self.root, text='Обложка проекта', font='Times 15')
        self.card_title.place(relx=.2)

        self.project_name = Label(self.root, text='*Название проекта*', font='Times 15')
        self.project_name.place(relx=.2, y=30)

        self.project_number = Label(self.root, text='№*num*', font='Times 15')
        self.project_number.place(relx=.7, y=15)

        self.vacancies_number = Label(
            self.root,
            text='*num_of_vac*\n свободных вакансий',
            borderwidth=2,
            relief="groove",
            font='Times 13'
        )
        self.vacancies_number.place(relx=.05, rely=.25)

        self.project_status = Label(
            self.root,
            text='*status*',
            borderwidth=2,
            relief='groove',
            font='Times 13'
        )
        self.project_status.place(relx=.05, rely=.4)

        self.project_head_title = Label(
            self.root,
            text='Руководитель:',
            font='Times 15'
        )
        self.project_head_title.place(x=10, rely=.6)

        self.project_head_name = Label(self.root, text='*name*:', font='Times 13')
        self.project_head_name.place(x=20, rely=.65)

        self.project_type_title = Label(self.root, text='Тип:', font='Times 15')
        self.project_type_title.place(x=10, rely=.75)

        self.project_type = Label(self.root, text='*type*:', font='Times 13')
        self.project_type.place(x=20, rely=.80)

        self.about_button = Button(self.root, text='Подробнее', command=self.__about_project())
        self.about_button.place(relx=.7, rely=.65, relheight=.1, relwidth=.2)

    def __about_project(self):
        self.about_window = Toplevel(self.root)
        self.about_window.geometry('400x400')
        self.about_window.title('Подробнее')

        self.wiki_img = ImageTk.PhotoImage(Image.open('drawables/ic_wiki.png'))
        self.wiki_button = Button(self.about_window, image=self.wiki_img, command=self.__wiki())
        self.wiki_button.place(relx=.5, rely=.05, relheight=.1, relwidth=.2)

        self.mail_img = ImageTk.PhotoImage(Image.open('drawables/ic_email.png'))
        self.mail_button = Button(self.about_window, image=self.mail_img)
        self.mail_button.place(relx=.65, rely=.05, relheight=.1, relwidth=.2)

        self.back = Button(self.about_window, text='Назад', command=self.about_window.destroy())
        self.back.place(relx=.55, rely=.3, relheight=.1, relwidth=.2)

        self.project_number = Label(self.about_window, text='Проект #', font='Times 15')
        self.project_number.place(x=10, y=10)

        self.project_type = Label(self.about_window, text=', *type*', font='Times 15')
        self.project_type.place(x=100, y=10)

        self.project_name = Label(self.about_window, text='*название проекта*', font='Times 15')
        self.project_name.place(x=10, y=50)

        self.project_type = Label(self.about_window, text='*статус*', font='Times 13')
        self.project_type.place(x=30, y=90)

        self.project_year = Label(self.about_window, text='*год*', font='Times 13')
        self.project_year.place(x=30, y=130)

        self.notebook = Notebook(self.about_window)
        self.notebook.place(rely=.4)

        # Frames
        self.first_frame = Frame(self.notebook, width=400, height=200)
        self.second_frame = Frame(self.notebook, width=400, height=200)
        self.third_frame = Frame(self.notebook, width=400, height=200)
        self.fourth_frame = Frame(self.notebook, width=400, height=200)
        self.notebook.add(self.first_frame, text='Общая информация')
        self.notebook.add(self.second_frame, text='Вакансии')
        self.notebook.add(self.third_frame, text='Команда')
        self.notebook.add(self.fourth_frame, text='Статистика')

        # FRAME 1
        # помещение текста в первое окно + перенос строк

        text_info = ''

        self.text_info_widget = Text(self.first_frame, width=45, height=30)
        self.text_info_widget.place(x=0, y=0)
        self.text_info_widget.config(
            foreground="black",
            font='times 12 ',
            wrap='word'
        )
        self.text_info_widget.insert(END, text_info)

        self.text_info_scroll = Scrollbar(self.first_frame, command=self.text_info_widget.yview)
        self.text_info_scroll.place(relx=.950, rely=.4)
        self.text_info_widget.config(yscrollcommand=self.text_info_scroll.set)

        # FRAME 2
        # помещение текста в первое окно + перенос строк

        text_vacancies = ''

        self.text_vacancies_widget = Text(self.second_frame, width=45, height=30)
        self.text_vacancies_widget.place(x=0, y=0)
        self.text_vacancies_widget.config(
            foreground='black',
            font='times 12 ',
            wrap='word')
        self.text_vacancies_widget.insert(END, text_vacancies)

        self.text_vacancies_scroll = Scrollbar(self.second_frame, command=self.text_vacancies_widget.yview)
        self.text_vacancies_scroll.place(relx=.950, rely=.4)
        self.text_vacancies_widget.config(yscrollcommand=self.text_vacancies_scroll.set)

        # FRAME 3
        # помещение текста в первое окно + перенос строк

        text_team = ''

        self.text_team_widget = Text(self.third_frame, width=45, height=30)
        self.text_team_widget.place(x=0, y=0)
        self.text_team_widget.config(
            foreground='black',
            font='times 12 ',
            wrap='word')
        self.text_team_widget.insert(END, text_team)

        self.text_team_scroll = Scrollbar(self.third_frame, command=self.text_team_widget.yview)
        self.text_team_scroll.place(relx=.950, rely=.4)
        self.text_team_widget.config(yscrollcommand=self.text_team_scroll.set)

        # FRAME 4
        # помещение текста в первое окно + перенос строк

        text_stats = ''

        self.text_stats_widget = Text(self.fourth_frame, width=45, height=30)
        self.text_stats_widget.place(x=0, y=0)
        self.text_stats_widget.config(
            foreground="black",
            font='times 12 ',
            wrap='word'
        )
        self.text_stats_widget.insert(END, text_stats)

        self.text_stats_scroll = Scrollbar(self.fourth_frame, command=self.text_stats_widget.yview)
        self.text_stats_scroll.place(relx=.950, rely=.4)
        self.text_stats_widget.config(yscrollcommand=self.text_stats_scroll.set)


root = Tk()
root.geometry("1280x720")
app = App(root=root, session=get_session(engine))
root.mainloop()
