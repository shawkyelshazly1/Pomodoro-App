from pomodoros_add_task import AddTaskWindow
import tkinter as tk
import json
from tkinter.constants import E
from labels import Task


class TasksWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.title("Tasks")
        self.geometry("500x300")
        self.db_object = None
        self.grid_columnconfigure((0, 2), weight=1)
        self.create_frame()
        self.load_tasks()
        self.create_widget()

    def create_task_label(self, task, id, i,):
        self.task = Task(
            self.content, task['task_title'], task['pomodoros'], id, self)
        self.task.grid(column=0, row=i, pady=5, columnspan=3, sticky='nsew')

    def load_db(self):
        try:
            with open('db.txt') as json_db:
                try:
                    self.data_obj = json.load(json_db)
                except:
                    self.data_obj = {}
                    self.data_obj['tasks'] = {}
                    with open('db.txt', 'w') as json_db:
                        json.dump(self.data_obj, json_db)

        except FileNotFoundError:
            json_db = open('db.txt', 'a+')
            self.load_db()

    def load_tasks(self):
        self.load_db()
        i = 0
        for id, task in self.data_obj['tasks'].items():
            self.create_task_label(task, id, i)
            i += 1

    def add_task(self, title, pomodors):
        id = len(self.data_obj['tasks'])+1
        task = {'task_title': title, 'pomodoros': pomodors}
        self.data_obj['tasks'][id] = task
        try:
            with open('db.txt', 'w') as json_db:
                json.dump(self.data_obj, json_db)
            self.create_task_label(task, id, len(self.data_obj['tasks'])-1)
        except:
            print('error')

    def remove_task(self, id):

        self.data_obj['tasks'].pop(id)
        with open('db.txt', 'w') as json_db:
            json.dump(self.data_obj, json_db)

    def create_frame(self):
        self.content = tk.Frame(self)
        self.content.grid(column=0, row=0, sticky='nsew')
        self.content.grid_columnconfigure((0, 4), weight=1)

    def create_widget(self):
        self.add_task_button = tk.Button(
            self, text="New Task", command=lambda: AddTaskWindow(self, self))
        self.add_task_button.grid(
            column=0, row=1, sticky='nsew', columnspan=3, padx=15)
