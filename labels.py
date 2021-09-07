import tkinter as tk


class Task(tk.Frame):
    def __init__(self, master=None, task_title=None, pomodoros_count=None, id=None, controller=None):
        super().__init__(master)
        self.id = id
        self.active_task_id = None
        self.controller = controller
        self.master = master
        self.title = tk.Label(self, text="Task: " + task_title)
        self.pomodoros = tk.Label(
            self, text="Pomodoros: " + str(pomodoros_count) + " 🍅")
        self.delete_button = tk.Button(
            self, text="Remove", command=self.delete_task)
        if self.controller.active_task_id == self.id:
            self.activate_button = tk.Button(
                self, text="Stop Task", command=self.activate_task)
        else:
            self.activate_button = tk.Button(
                self, text="Activate", command=self.activate_task)

        self.title.grid(column=0, row=0, sticky='nw', padx=5)
        self.pomodoros.grid(column=1, row=0, sticky='ne', padx=5)
        self.delete_button.grid(column=2, row=0, sticky='ne')
        self.activate_button.grid(column=3, row=0, sticky='ne')

    def delete_task(self):
        self.controller.remove_task(self.id)
        self.grid_remove()

    def activate_task(self):
        if self.controller.active_task_id == None:
            self.controller.active_task_id = self.id
            self.controller.activate_task(self.id)

        else:
            if self.id == self.controller.active_task_id:
                self.controller.stop_task()
                self.controller.active_task_id = None
            else:
                self.controller.active_task_id = self.id
                self.controller.activate_task(self.id)
