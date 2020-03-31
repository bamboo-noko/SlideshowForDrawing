import tkinter as tk
import os
from slideshowservice import SlideshowService
import random
import glob
from tkinter import filedialog
import datetime
import json
import ast
import re
from PIL import Image, ImageTk, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from history import History
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.serivce = SlideshowService()
        self.master = master
        self.pack()
        self.repeat_num = 0
        self.indexes = []
        self.index = 0
        self.history = History()
        self.history_list = []
        self.create_menu()
        self.elapsed_time = 0
        self.tick = 1
        self.create_widgets()
        self.after_id = 0
        self.is_puase = False

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=fileMenu)
        optionMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Option", menu=optionMenu)

        fileMenu.add_command(label="save", command=self.save_config)
        fileMenu.add_command(label="open", command=self.open_config)
        optionMenu.add_command(label="report", command=self.report)

    def create_widgets(self):
        self.canvas_width = 1000
        self.canvas_height = 500

        self.select_directory_frame = tk.Frame(self)
        self.select_directory_frame.pack(fill="x")
        self.input_directory = tk.Entry(self.select_directory_frame, width=200)
        self.input_directory.pack(side="left")
        self.button_open_directory = tk.Button(self.select_directory_frame, text="open", command=self.open_image)
        self.button_open_directory.pack(side="left")

        self.practice_menu_frame = tk.Frame(self)
        self.practice_menu_frame.pack(fill="x")
        self.label_repeat_num = tk.Label(self.practice_menu_frame, text=u'セット数')
        self.label_repeat_num.pack(side="left")
        self.input_repeat_num = tk.Entry(self.practice_menu_frame, width=10)
        self.input_repeat_num.pack(side="left")
        self.label_time_limit = tk.Label(self.practice_menu_frame, text=u'表示時間(秒)')
        self.label_time_limit.pack(side="left")
        self.input_time_limit = tk.Entry(self.practice_menu_frame, width=10)
        self.input_time_limit.pack(side="left")

        self.is_random = tk.BooleanVar()
        self.check_random = tk.Checkbutton(self.practice_menu_frame, text="ランダム", variable=self.is_random)
        self.check_random.pack(side="left")
        self.is_mirror = tk.BooleanVar()
        self.check_mirror = tk.Checkbutton(self.practice_menu_frame, text="左右反転", variable=self.is_mirror)
        self.check_mirror.pack(side="left")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill="x")
        self.button_start = tk.Button(self.button_frame, text="start", command=self.start)
        self.button_start.pack(side="left")
        self.button_pause = tk.Button(self.button_frame, text="pause", command=self.pause)
        self.button_pause.pack(side="left")
        self.button_pause["state"] = "disabled"
        self.button_stop = tk.Button(self.button_frame, text="stop", command=self.stop)
        self.button_stop.pack(side="left")
        self.button_stop["state"] = "disabled"
        self.button_next = tk.Button(self.button_frame, text="next", command=self.next)
        self.button_next.pack(side="left")
        self.button_next["state"] = "disabled"
        self.number_of_times_remaining = tk.Label(self.button_frame)
        self.number_of_times_remaining["text"] = self.repeat_num
        self.number_of_times_remaining.pack(side="left")
        self.string_var_time_limit = tk.StringVar()
        self.time_limit = tk.Label(self.button_frame, textvariable=self.string_var_time_limit)
        self.time_limit["text"] = 0
        self.time_limit.pack(side="left")

        self.photo = tk.PhotoImage()
        self.canvas = tk.Canvas(bg="black", width=self.canvas_width, height=self.canvas_height)
        # self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        root.bind('<Configure>', self.resize)

    def start(self):
        if not self.is_ready():
            return

        self.ready()
        image = self.get_next_image()
        self.display_image(image)
        self.create_history()
        self.after(self.tick * 1000, self.timer_event)

    def is_ready(self):
        if not os.path.exists(self.input_directory.get()):
            print("path not exists.")
            return False
        
        if not self.input_repeat_num.get():
            print("please input repeat num.")
            return False

        if self.input_repeat_num.get() == '0':
            print("please input repeat num.")
            return False

        try:
            int(self.input_repeat_num.get())
        except ValueError:
            print("please input numeric.")
            return False

        if not self.input_time_limit.get():
            print("please input time limit.")
            return False

        try:
            int(self.input_time_limit.get())
        except ValueError:
            print("please input numeric.")
            return False

        if not self.input_time_limit.get().isdecimal():
            print("please input numeric.")
            return False

        return True

    def ready(self):
        self.repeat_num = int(self.input_repeat_num.get())
        self.index = -1
        self.indexes = [i for i in range(len(self.file_paths))]
        self.time_limit["text"] = self.input_time_limit["text"]
        self.current_time = self.input_time_limit["text"]
        self.string_var_time_limit.set(int(self.input_time_limit.get()))
        self.number_of_times_remaining["text"] = self.repeat_num
        self.input_directory["state"] = "disabled"
        self.input_repeat_num["state"] = "disabled"
        self.input_time_limit["state"] = "disabled"        
        self.button_open_directory["state"] = "disabled"
        self.check_mirror["state"] = "disabled"
        self.check_random["state"] = "disabled"
        self.button_start["state"] = "disabled"
        self.button_stop["state"] = "normal"
        self.button_next["state"] = "normal"
        self.button_pause["state"] = "normal"

        if self.is_random.get():
            random.shuffle(self.indexes)

    def get_next_image(self):
        self.index = self.serivce.get_next_image_index(self.index, len(self.file_paths))
        im = Image.open(self.file_paths[self.indexes[self.index]])
        return im

    def timer_event(self):
        self.after_id = self.after(self.tick * 1000, self.timer_event)
        self.string_var_time_limit.set(int(self.string_var_time_limit.get()) - self.tick)
        if int(self.string_var_time_limit.get()) > 0:
            return

        self.string_var_time_limit.set(self.input_time_limit.get())
        self.repeat_num -= 1
        self.number_of_times_remaining["text"] = self.repeat_num
        self.history.end_time = datetime.datetime.today()
        self.history_list.append(self.history)
        if self.repeat_num <= 0:
            self.end()
            return

        image = self.get_next_image()
        self.display_image(image)
        self.create_history()

    def end(self):
        self.photo = tk.PhotoImage()
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.after_cancel(self.after_id)
        self.repeat_num = 0
        self.input_directory["state"] = "normal"
        self.input_repeat_num["state"] = "normal"
        self.input_time_limit["state"] = "normal"        
        self.button_open_directory["state"] = "normal"
        self.check_mirror["state"] = "normal"
        self.check_random["state"] = "normal"
        self.button_start["state"] = "normal"
        self.button_stop["state"] = "disabled"
        self.button_next["state"] = "disabled"
        self.button_pause["state"] = "disabled"
        self.save_history()
        self.history_list.clear()

    def open_image(self):
        select_directory_path = filedialog.askdirectory()
        self.file_paths = [p for p in glob.glob(select_directory_path + "/*.*")
            if re.search('.*\.(png|jpg)', str(p))]
        self.input_directory.delete(0, tk.END)
        self.input_directory.insert(tk.END, select_directory_path)

    def resize(self, event):
        self.canvas_height = event.height
        self.canvas_width = event.width

    def create_history(self):
        self.history = History()
        self.history.file_path = self.file_paths[self.indexes[self.index]]
        self.history.time_limit = self.input_time_limit.get()
        self.history.start_time = datetime.datetime.today()
        self.history.create_datetime = datetime.datetime.today()

    def display_image(self, image):
        if self.is_mirror.get() and random.randrange(0, 2) == 1:
            image = ImageOps.mirror(image)
        image_tk = ImageTk.PhotoImage(image)
        self.photo = image_tk
        
        self.canvas.create_image(self.master.winfo_width()/2, self.canvas.winfo_height()/2, image=image_tk, anchor=tk.CENTER)

    def save_config(self):
        current_settings = []
        current_settings.append(self.input_directory.get())
        current_settings.append(self.input_repeat_num.get())
        current_settings.append(self.input_time_limit.get())
        current_settings.append(str(self.is_random.get()))
        current_settings.append(str(self.is_mirror.get()))

        fname = tk.filedialog.asksaveasfilename()
        if not fname:
            return

        with open(fname, 'w', encoding="utf-8") as f:
            f.write(','.join(current_settings))

    def open_config(self):
        select_directory_path = filedialog.askopenfilename()
        if not select_directory_path:
            return

        if select_directory_path:
            with open(select_directory_path, 'r', encoding="utf-8") as f:
                self.input_directory.delete(0, tk.END)
                self.input_repeat_num.delete(0, tk.END)
                self.input_time_limit.delete(0, tk.END)

                csv = f.readline().split(",")
                self.input_directory.insert(tk.END, csv[0])
                self.input_repeat_num.insert(tk.END, csv[1])
                self.input_time_limit.insert(tk.END, csv[2])
                self.is_random.set(csv[3])
                self.is_mirror.set(csv[4])

                self.file_paths = glob.glob(self.input_directory.get() + "/*.png")

    def stop(self):
        self.history.end_time = datetime.datetime.today()
        self.history_list.append(self.history)

        self.end()

    def next(self):
        self.after_cancel(self.after_id)
        self.string_var_time_limit.set(1)
        self.timer_event()

    def pause(self):
        if self.is_puase:
            self.is_puase = False
            self.after(self.tick * 1000, self.timer_event)
            self.button_pause["text"] = "pause"
            self.button_stop["state"] = "normal"
            self.button_next["state"] = "normal"
        else:
            self.is_puase = True
            self.after_cancel(self.after_id)
            self.button_next["state"] = "disabled"
            self.button_stop["state"] = "disabled"
            self.button_pause["text"] = "resume"

    def save_history(self):
        save_filename = "history.csv"
        filepath = "history/{}".format(save_filename)

        csv_list = []
        for history in self.history_list:
            csv = []
            csv.append(history.file_path.replace('\\','/'))
            csv.append(history.time_limit)
            csv.append(history.start_time.isoformat())
            csv.append(history.end_time.isoformat())
            diff_time = history.end_time - history.start_time
            csv.append(str(diff_time))
            csv.append(history.create_datetime.isoformat())
            csv_list.append(",".join(csv))

        if os.path.exists(filepath):
            with open("history/"+save_filename, 'a', encoding="utf-8") as f:
                f.write('\n')
                f.write("\n".join(csv_list))
        else:
            with open("history/"+save_filename, 'a', encoding="utf-8") as f:
                f.write("\n".join(csv_list))

    def report(self):
        self.dialog = tk.Toplevel()
        self.dialog.title("modal dialog")
        self.dialog.geometry("300x300")
        self.dialog.grab_set()

        service = SlideshowService()
        history_list = service.get_history_all("history.csv")
        history_dict = service.get_report(history_list)
        fig = service.create_graph(history_dict)
        canvas = FigureCanvasTkAgg(fig, self.dialog)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

root = tk.Tk()
root.state('zoomed')
app = Application(master=root)
app.mainloop()