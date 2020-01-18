import tkinter as tk
import os
import random
import glob
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.repeat_num = 0
        self.indexes = []
        self.index = 0
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=fileMenu)
        editMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editMenu)

        fileMenu.add_command(label="save", command=self.save_config)
        fileMenu.add_command(label="open", command=self.open_config)

    def create_widgets(self):
        self.canvas_width = 1000
        self.canvas_height = 500

        self.select_directory_frame = tk.Frame(self)
        self.select_directory_frame.pack(fill="x")
        self.input_directory = tk.Entry(self.select_directory_frame, width=200)
        self.input_directory.pack(side="left")
        self.button_read_directory = tk.Button(self.select_directory_frame, text="read", command=self.read_image)
        self.button_read_directory.pack(side="left")

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

        self.button_start = tk.Button(self, text="start", command=self.start)
        self.button_start.pack()

        self.photo = tk.PhotoImage()
        self.canvas = tk.Canvas(bg="black", width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        root.bind('<Configure>', self.resize)

    def start(self):
        self.repeat_num = int(self.input_repeat_num.get())
        self.index = 0
        self.indexes = [i for i in range(len(self.file_paths))]
        if self.is_random.get():
            random.shuffle(self.indexes)
        self.timer_event()

    def timer_event(self):
        self.repeat_num -= 1
        if self.repeat_num < 0:
            return

        self.change_image()
        self.index += 1
        self.after(int(self.input_time_limit.get()) * 1000, self.timer_event)

    def read_image(self):
        select_directory_path = filedialog.askdirectory()
        self.file_paths = glob.glob(select_directory_path + "/*.png")
        self.input_directory.delete(0, tk.END)
        self.input_directory.insert(tk.END, select_directory_path)

    def resize(self, event):
        self.canvas_height = event.height
        self.canvas_width = event.width

    def change_image(self):
        self.photo = tk.PhotoImage(file=self.file_paths[self.indexes[self.index]])
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def save_config(self):
        current_settings = []
        current_settings.append(self.input_directory.get())
        current_settings.append(self.input_repeat_num.get())
        current_settings.append(self.input_time_limit.get())
        current_settings.append(str(self.is_random.get()))

        fname = tk.filedialog.asksaveasfilename()
        if not fname:
            return

        with open(fname, 'a', encoding="utf-8") as f:
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

                self.file_paths = glob.glob(self.input_directory.get() + "/*.png")


root = tk.Tk()
root.state('zoomed')
app = Application(master=root)
app.mainloop()