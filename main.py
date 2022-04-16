from tkinter import *

from scripts.gui import App
from scripts.create_tables import get_session, engine, create_tables


def main():
    create_tables(engine)

    root = Tk()
    root.geometry("650x720")
    app = App(root=root, session=get_session(engine))
    root.mainloop()


if __name__ == '__main__':
    main()
