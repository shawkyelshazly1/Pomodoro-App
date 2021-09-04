import tkinter as tk
import json
from tkinter.constants import E
from labels import Task


class AddTaskWindow(tk.Toplevel):
    def __init__(self, master=None, controller=None):
        super().__init__(master=master)
        self.master = master
        self.controller = controller
        self.title("Tasks")
        self.geometry("400x200")
        self.error_text = tk.StringVar(value="")
        self.create_widgets()

    def create_widgets(self):
        self.task_title_label = tk.Label(self, text='Task Title')
        self.task_title_label.grid(column=1, row=0)
        self.task_title_entry = tk.Entry(self)
        self.task_title_entry.grid(column=2, row=0)

        self.task_pomodoro_label = tk.Label(self, text='Pomodoros 🍅')
        self.task_pomodoro_label.grid(column=1, row=1)
        self.task_pomodoro_entry = tk.Entry(self)
        self.task_pomodoro_entry.grid(column=2, row=1)

        self.error_label = tk.Label(self, textvariable=self.error_text)
        self.error_label.grid(column=1, row=2, columnspan=2)

        self.add_task_button = tk.Button(
            self, text="Add Task", command=self.add_task)

        self.add_task_button.grid(column=1, row=3, columnspan=2, pady=15)

    def add_task(self):
        if self.validate_input():
            self.controller.add_task(
                self.task_title_entry.get(), self.task_pomodoro_entry.get())
            self.destroy()

    def validate_input(self):
        if len(self.task_title_entry.get()) < 1 or str.isspace(self.task_title_entry.get()):
            self.error_text.set("Task Title can't be empty!")
            return False
        elif len(self.task_pomodoro_entry.get()) < 1:
            self.error_text.set("please enter number of pomodoros!")
            return False
        else:
            try:
                pomodoros = int(self.task_pomodoro_entry.get())
                if pomodoros > 0:
                    return True
                else:
                    self.error_text.set(
                        "please enter a valid number of pomodoros not 0!")
            except:
                self.error_text.set(
                    "please enter a valid number of pomodoros!")
                return False
