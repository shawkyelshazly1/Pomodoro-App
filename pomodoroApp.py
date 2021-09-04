#!/home/shaq/projects/pomodoro/env/bin/python

import time
from playsound import playsound
from tkinter.constants import NSEW, TOP
import tkinter as tk
import json


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.init_vars()
        self.create_Frames()
        self.create_widgets()
        self.load_db()

    def create_Frames(self):
        self.content = tk.Frame(self, bg='#ff7575')
        self.content.grid(column=0, row=0, sticky='nsew')
        self.content.grid_columnconfigure((0, 2), weight=1)
        self.content.grid_rowconfigure((0, 4), weight=1)

    def create_widgets(self):
        self.pomodoro_btn = tk.Button(
            self.content, text="Pomodoro", borderwidth=0, command=self.start_pomo, fg='#fff', bg='#ff7575',)
        self.pomodoro_btn.grid(column=0, row=0, sticky='n', pady=15)

        self.short_break_btn = tk.Button(
            self.content, text="Short Break", border=0, command=self.start_short_break, fg='#fff', bg='#ff7575')
        self.short_break_btn.grid(column=1, row=0, sticky='n', pady=15)

        self.long_break_btn = tk.Button(
            self.content, text="Long Break", border=0, command=self.start_long_break, fg='#fff', bg='#ff7575')
        self.long_break_btn.grid(column=2, row=0, sticky='n', pady=15)

        self.timer_label = tk.Label(self.content, textvariable=self.timer,
                                    fg='#fff', bg='#ff7575', font=('arial', 90))
        self.timer_label.grid(
            column=0, row=1, columnspan=3, rowspan=2, sticky='n')

        self.start_button = tk.Button(
            self.content, text="START", fg='#fff', bg='#ff7575', border=0, width=10, font=('arial', 50), command=self.start_timer)
        self.start_button.grid(
            column=0, row=3, columnspan=3, rowspan=2, sticky='s', pady=20)

    def start_pomo(self):
        self.timer.set('25:00')
        self.activity.set('pomo')
        self.duration.set(1500)
        self.adjust_widgets_color()

    def start_long_break(self):
        self.timer.set('15:00')
        self.activity.set('long')
        self.duration.set(900)
        self.adjust_widgets_color()

    def start_short_break(self):
        self.timer.set('05:00')
        self.activity.set('short')
        self.duration.set(300)
        self.adjust_widgets_color()

    def adjust_color(self, color):
        self.content.configure(background=color)
        self.pomodoro_btn.configure(background=color)
        self.short_break_btn.configure(background=color)
        self.long_break_btn.configure(background=color)
        self.timer_label.configure(background=color)
        self.start_button.configure(background=color)

    def adjust_widgets_color(self):
        if self.activity.get() == 'pomo':
            self.adjust_color('#ff7575')
        elif self.activity.get() == 'long':
            self.adjust_color('#2eb2ff')
        elif self.activity.get() == 'short':
            self.adjust_color('#618bff')

    def init_vars(self):
        self.timer = tk.StringVar(value='25:00')
        self.activity = tk.StringVar(value='pomo')
        self.duration = tk.IntVar(value=1500)
        self.timer_id = tk.StringVar()
        self.started_flag = False
        self.pomodoros = 0
        self.db_object = None

    def start_timer(self):
        self.started_flag = True
        self.switch_controlles()
        self.start_button.configure(text='STOP', command=self.stop_timer)
        self.update_timer(self.duration.get())

    def update_timer(self, duration):
        if duration >= 0:
            duration_seconds = duration
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60

            if seconds < 10:
                seconds_txt = f"0{seconds}"
            else:
                seconds_txt = f"{seconds}"

            if minutes < 10:
                minutes_txt = f"0{minutes}"
            else:
                minutes_txt = f"{minutes}"

            self.timer.set(f"{minutes_txt}:{seconds_txt}")
            duration_seconds -= 1
            id = self.after(
                1000, lambda: self.update_timer(duration_seconds))
            self.timer_id.set(id)
        else:
            self.switch_activity()

    def switch_activity(self):
        if self.activity.get() == 'pomo':
            self.pomodoros += 1

        if self.activity.get() == 'pomo':
            if self.pomodoros % 4 == 0:
                playsound('./assets/alarm-bell.mp3')
                time.sleep(1)
                self.start_long_break()
                self.start_timer()
            else:
                playsound('./assets/alarm-wood.mp3')
                time.sleep(1)
                self.start_short_break()
                self.start_timer()
        else:
            playsound('./assets/alarm-digital.mp3')
            time.sleep(1)
            self.start_pomo()
            self.start_timer()

    def switch_controlles(self):
        if self.started_flag:
            self.pomodoro_btn.configure(state='disabled')
            self.short_break_btn.configure(state='disabled')
            self.long_break_btn.configure(state='disabled')
            self.adjust_widgets_color()
        else:
            self.pomodoro_btn.configure(state='active')
            self.short_break_btn.configure(state='active')
            self.long_break_btn.configure(state='active')
            self.adjust_widgets_color()

    def stop_timer(self):
        self.after_cancel(self.timer_id.get())
        self.started_flag = False
        self.switch_controlles()
        self.start_button.configure(text='START', command=self.start_timer)

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

    def add_task(self, title, pomodors):
        id = len(self.data_obj['tasks'])+1
        task = {id: {'task_title': title, 'pomodoros': pomodors}}
        self.data_obj['tasks'][id] = task
        try:
            with open('db.txt', 'w') as json_db:
                json.dump(self.data_obj, json_db)
        except:
            print('error')

    def remove_task(self, id):
        self.data_obj['tasks'].pop(str(id))
        try:
            with open('db.txt', 'w') as json_db:
                json.dump(self.data_obj, json_db)
        except:
            print('error')


if __name__ == "__main__":
    pomodoro_app = App()
    pomodoro_app.title("Pomodoro App")
    pomodoro_app.geometry("600x400")
    pomodoro_app.mainloop()
