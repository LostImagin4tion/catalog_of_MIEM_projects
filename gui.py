from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Каталог проектов')

        self.projects_list = Listbox(selectmode=EXTENDED, height=15, width=60)
        project_values = ['*Пример проекта*']

        for value in project_values:
            self.projects_list.insert(END, value)

        self.projects_list.place(x=9, y=110)
        self.project_scroll = Scrollbar(command=self.projects_list.yview)
        self.project_scroll.place(x=380, y=200)
        self.projects_list.config(yscrollcommand=self.project_scroll.set)

        self.projects_list.bind('<<ListboxSelect>>', self.__on_click_projects_list())

        self.canvas = Canvas(self.root, width=400, height=400)

        self.find_field = Entry(root, width=40)
        self.find_field.insert(0, 'Введите номер, название или руководителя проекта')
        self.find_field.grid(column=1, padx=15, pady=15, columnspan=5, row=0)

        self.mag = PhotoImage(file='drawables/ic_search.png')
        self.find_button = Button(root, image=self.mag, command=self.__search())
        self.find_button.grid(column=6, columnspan=1, row=0)

        self.update_img = PhotoImage(file='drawables/ic_update.png')
        self.update_button = Button(root, image=self.update_img, command=self.__update())
        self.update_button.grid(column=7, columnspan=1, padx=10, row=0)

        self.export_img = PhotoImage(file='drawables/ic_export.png')
        self.export_button = Button(root, image=self.export_img, command=self.__export())
        self.export_button.grid(column=8, columnspan=1, row=0)

        self.sort_top = Label(root, text='Сортировать по:')

        self.sort_value = Combobox(root, values=[
            '*sort_cond1*',
            '*sort_cond2*',
            '*sort_cond3*',
            '*sort_cond4*'
        ])

        self.sort_top.grid(column=1, row=2)
        self.sort_value.grid(column=1, row=3)
        self.sort_value.current(0)

        self.filter_top = Label(root, text='Фильтр:')
        self.filter_top.grid(column=3, row=2)

        filter_values = ['*filter_cond*', '*filter_cond*', '*filter_cond*', '*filter_cond*', '*filter_cond*', 'filter_cond*']
        self.filter_box = Listbox(selectmode=MULTIPLE, height=len(filter_values))
        for value in filter_values:
            self.filter_box.insert(END, value)

        self.filter_button = Button(root, text='Фильтровать по:', command=lambda: self.filter_box.place(x=160, y=90))
        self.filter_button.place(x=160, y=65)

        self.hide_filters_button = Button(root, text='Скрыть фильтр', command=lambda: self.filter_box.place_forget())
        self.hide_filters_button.place(x=260, y=65)

        # self.filter_box.place(x=170, y=65)
        self.scroll = Scrollbar(command=self.filter_box.yview)
        self.filter_box.config(yscrollcommand=self.scroll.set)

    def __search(self):
        return 0

    def __wiki(self):
        return 0

    def __update(self):
        return 0

    def __export(self):
        return 0

    def __on_click_projects_list(self, event):

        self.project_card_window = Toplevel(root)
        self.project_card_window.geometry("400x400")

        self.back = Button(self.project_card_window, text='Назад', command=self.project_card_window.destroy)
        self.back.place(relx=.7, rely=.8, relheight=.1, relwidth=.2)

        self.project_card_window.title('Карточка проекта')

        self.card_title = Label(self.project_card_window, text='Обложка проекта', font='Times 15')
        self.card_title.place(relx=.2)

        self.project_name = Label(self.project_card_window, text='*Название проекта*', font='Times 15')
        self.project_name.place(relx=.2, y=30)

        self.project_number = Label(self.project_card_window, text='№*num*', font='Times 15')
        self.project_number.place(relx=.7, y=15)

        self.vacancies_number = Label(
            self.project_card_window,
            text='*num_of_vac*\n свободных вакансий',
            borderwidth=2,
            relief="groove",
            font='Times 13'
        )
        self.vacancies_number.place(relx=.05, rely=.25)

        self.project_status = Label(
            self.project_card_window,
            text='*status*',
            borderwidth=2,
            relief='groove',
            font='Times 13'
        )
        self.project_status.place(relx=.05, rely=.4)

        self.project_head_title = Label(
            self.project_card_window,
            text='Руководитель:',
            font='Times 15'
        )
        self.project_head_title.place(x=10, rely=.6)

        self.project_head_name = Label(self.project_card_window, text='*name*:', font='Times 13')
        self.project_head_name.place(x=20, rely=.65)

        self.project_type_title = Label(self.project_card_window, text='Тип:', font='Times 15')
        self.project_type_title.place(x=10, rely=.75)

        self.project_type = Label(self.project_card_window, text='*type*:', font='Times 13')
        self.project_type.place(x=20, rely=.80)

        self.about_button = Button(self.project_card_window, text='Подробнее', command=self.__about_project())
        self.about_button.place(relx=.7, rely=.65, relheight=.1, relwidth=.2)

    def __about_project(self):
        self.about_window = Toplevel(self.project_card_window)
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
root.geometry("400x400")
app = App(root)
root.mainloop()
