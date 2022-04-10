from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Каталог проектов")

        self.projects_list = Listbox(selectmode=EXTENDED, height=15, width=60)
        project_values = ["*Пример проекта*"]

        for value in project_values:
            self.projects_list.insert(END, value)

        self.projects_list.place(x=9, y=110)
        self.projectScroll = Scrollbar(command=self.projects_list.yview)
        self.projectScroll.place(x=380, y=200)
        self.projects_list.config(yscrollcommand=self.projectScroll.set)

        self.projects_list.bind('<<ListboxSelect>>', self.onClickProjectList)

        self.canvas = Canvas(self.root, width=400, height=400)

        self.findField = Entry(root, width=40)
        self.findField.insert(0, "Введите номер или название проекта")
        self.findField.grid(column=1, padx=15, pady=15, columnspan=5, row=0)

        self.mag = PhotoImage(file='drawables/ic_search.png')
        self.findButton = Button(root, image=self.mag, command=self.search())
        self.findButton.grid(column=6, columnspan=1, row=0)
        self.wikiButton = PhotoImage(file='вики.png')

        self.renewimg = PhotoImage(file='drawables/ic_update.png')
        self.renewButton = Button(root, image=self.renewimg, command=self.renew)
        self.renewButton.grid(column=7, columnspan=1, padx=10, row=0)

        self.docimg = PhotoImage(file='drawables/ic_export.png')
        self.docButton = Button(root, image=self.docimg, command=self.doc)
        self.docButton.grid(column=8, columnspan=1, row=0)

        self.sortTop = Label(root,
                             text="Сортировать по:")

        self.sortValue = Combobox(root,
                                  values=[
                                      "*sort_cond1*",
                                      "*sort_cond2*",
                                      "*sort_cond3*",
                                      "*sort_cond4*"])
        self.sortTop.grid(column=1, row=2)
        self.sortValue.grid(column=1, row=3)
        self.sortValue.current(0)

        self.filtrTop = Label(root,
                              text="Фильтр:")
        self.filtrTop.grid(column=3, row=2)

        filter_values = ["*filter_cond*", "*filter_cond*", "*filter_cond*", "*filter_cond*", "*filter_cond*", "filter_cond*"]
        self.FiltrBox = Listbox(selectmode=MULTIPLE, height=len(filter_values))
        for value in filter_values:
            self.FiltrBox.insert(END, value)

        self.filtrButton = Button(root, text="Фильтровать по:", command=lambda: self.FiltrBox.place(x=160, y=90))
        self.filtrButton.place(x=160, y=65)

        self.forgetButton = Button(root, text="Скрыть фильтр", command=lambda: self.FiltrBox.place_forget())
        self.forgetButton.place(x=260, y=65)

        # self.FiltrBox.place(x=170, y=65)
        self.scroll = Scrollbar(command=self.FiltrBox.yview)
        self.FiltrBox.config(yscrollcommand=self.scroll.set)

    def search(self):
        return 0

    def update(self):
        return 0

    def export(self):
        return 0

    def on_click_projects_list(self, event):

        self.projectCardWindow = Toplevel(root)
        self.projectCardWindow.geometry("400x400")

        self.back = Button(self.projectCardWindow, text="Назад", command=self.projectCardWindow.destroy)
        self.back.place(relx=.7, rely=.8, relheight=.1, relwidth=.2)

        self.projectCardWindow.title("Карточка проекта")

        self.titleCard = Label(self.projectCardWindow, text="Обложка проекта", font='Times 15')
        self.titleCard.place(relx=.2)

        self.nameProj = Label(self.projectCardWindow, text="*Название проекта*", font='Times 15')
        self.nameProj.place(relx=.2, y=30)

        self.numProj = Label(self.projectCardWindow, text="№*num*", font='Times 15')
        self.numProj.place(relx=.7, y=15)

        self.vac = Label(self.projectCardWindow, text="*num_of_vac*\n свободных вакансий", borderwidth=2,
                         relief="groove", font='Times 13')
        self.vac.place(relx=.05, rely=.25)

        self.typeVal = Label(self.projectCardWindow, text="*status*", borderwidth=2, relief="groove", font='Times 13')
        self.typeVal.place(relx=.05, rely=.4)

        self.lead = Label(self.projectCardWindow, text="Руководитель:", font='Times 15')
        self.lead.place(x=10, rely=.6)

        self.leadName = Label(self.projectCardWindow, text="*name*:", font='Times 13')
        self.leadName.place(x=20, rely=.65)

        self.type = Label(self.projectCardWindow, text="Тип:", font='Times 15')
        self.type.place(x=10, rely=.75)

        self.typeVal = Label(self.projectCardWindow, text="*type*:", font='Times 13')
        self.typeVal.place(x=20, rely=.80)

        self.about = Button(self.projectCardWindow, text="Подробнее", command=self.aboutProject)
        self.about.place(relx=.7, rely=.65, relheight=.1, relwidth=.2)

    def about_project(self):
        self.aboutWindow = Toplevel(self.projectCardWindow)
        self.aboutWindow.geometry("400x400")
        self.aboutWindow.title("Подробнее")

        self.imgWiki = ImageTk.PhotoImage(Image.open("drawables/ic_wiki.png"))
        self.panelWiki = Label(self.aboutWindow, image=self.imgWiki)
        self.panelWiki.place(relx=.5, rely=.05)

        self.wikiButton = Button(self.aboutWindow, text="Wiki")
        self.wikiButton.place(relx=.5, rely=.2, width=55, height=30)

        self.imgMail = ImageTk.PhotoImage(Image.open("drawables/ic_email.png"))
        self.panelMail = Label(self.aboutWindow, image=self.imgMail)
        self.panelMail.place(relx=.65, rely=.05)

        self.mailButton = Button(self.aboutWindow, text="Mail")
        self.mailButton.place(relx=.65, rely=.2, width=55, height=30)

        self.back = Button(self.aboutWindow, text="Назад", command=self.aboutWindow.destroy)
        self.back.place(relx=.55, rely=.3, relheight=.1, relwidth=.2)

        self.numberProj = Label(self.aboutWindow, text="Проект #", font='Times 15')
        self.numberProj.place(x=10, y=10)

        self.typeProj = Label(self.aboutWindow, text=", *type*", font='Times 15')
        self.typeProj.place(x=100, y=10)

        self.nameProj = Label(self.aboutWindow, text="*название проекта*", font='Times 15')
        self.nameProj.place(x=10, y=50)

        self.typeVal = Label(self.aboutWindow, text="*статус*", font='Times 13')
        self.typeVal.place(x=30, y=90)

        self.typeVal = Label(self.aboutWindow, text="*год*", font='Times 13')
        self.typeVal.place(x=30, y=130)

        self.notebook = Notebook(self.aboutWindow)
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
        text_info = ""

        self.textInfoWidjet = Text(self.first_frame, width=45, height=30)
        self.textInfoWidjet.place(x=0, y=0)
        self.textInfoWidjet.config(foreground="black",
                                   font='times 12 ', wrap='word')
        self.textInfoWidjet.insert(END, text_info)

        self.textInfoScroll = Scrollbar(self.first_frame, command=self.textInfoWidjet.yview)
        self.textInfoScroll.place(relx=.950, rely=.4)
        self.textInfoWidjet.config(yscrollcommand=self.textInfoScroll.set)

        # FRAME 2
        # помещение текста в первое окно + перенос строк

        text_vacancies = ""

        self.textVacWidjet = Text(self.second_frame, width=45, height=30)
        self.textVacWidjet.place(x=0, y=0)
        self.textVacWidjet.config(foreground="black",
                                  font='times 12 ', wrap='word')
        self.textVacWidjet.insert(END, text_vacancies)

        self.textVacScroll = Scrollbar(self.second_frame, command=self.textVacWidjet.yview)
        self.textVacScroll.place(relx=.950, rely=.4)
        self.textVacWidjet.config(yscrollcommand=self.textVacScroll.set)

        # FRAME 3
        # помещение текста в первое окно + перенос строк

        text_team = ""

        self.textComandWidjet = Text(self.third_frame, width=45, height=30)
        self.textComandWidjet.place(x=0, y=0)
        self.textComandWidjet.config(foreground="black",
                                     font='times 12 ', wrap='word')
        self.textComandWidjet.insert(END, text_team)

        self.textComandScroll = Scrollbar(self.third_frame, command=self.textComandWidjet.yview)
        self.textComandScroll.place(relx=.950, rely=.4)
        self.textComandWidjet.config(yscrollcommand=self.textComandScroll.set)

        # FRAME 4
        # помещение текста в первое окно + перенос строк

        text_stats = ""

        self.textStatWidjet = Text(self.fourth_frame, width=45, height=30)
        self.textStatWidjet.place(x=0, y=0)
        self.textStatWidjet.config(foreground="black",
                                   font='times 12 ', wrap='word')
        self.textStatWidjet.insert(END, text_stats)

        self.textStatScroll = Scrollbar(self.fourth_frame, command=self.textStatWidjet.yview)
        self.textStatScroll.place(relx=.950, rely=.4)
        self.textStatWidjet.config(yscrollcommand=self.textStatScroll.set)


root = Tk()
root.geometry("400x400")
app = App(root)
root.mainloop()
