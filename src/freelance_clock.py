import pyautogui
import datetime
import csv
import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

running = False
hours, minutes, seconds = 0, 0, 0
start_datehour, end_datehour = datetime.datetime.now(), datetime.datetime.now()
master_folder = ""
task_folder = ""
label = ""

def start():
    global running
    global master_folder
    global start_datehour
    global task_folder
    global label
    if not running:
        label = simpledialog.askstring(title="", prompt="What are you working on:")
        if label:
            start_datehour = datetime.datetime.now()
            task_folder = master_folder + \
                f"/{label}-" + \
                f"{start_datehour.year}-" + \
                f"{str(start_datehour.month).zfill(2)}-" + \
                f"{str(start_datehour.day).zfill(2)}-" + \
                f"{str(start_datehour.hour).zfill(2)}-" + \
                f"{str(start_datehour.minute).zfill(2)}-" + \
                f"{str(start_datehour.second).zfill(2)}"
    
            try:
                os.mkdir(task_folder)
            except:
                messagebox.showerror(
                    title="Error!", 
                    message="Something went wrong, try again."
                )

            pyautogui.screenshot().save(task_folder + f"/start.png")

            running = True
            button.config(text="stop", height=5, width=5, command=reset, font=('Arial', 30))
            update()
        
def reset():
    global running
    global start_datehour
    global end_datehour
    global hours, minutes, seconds
    global label
    if running:
        end_datehour = datetime.datetime.now()
        stopwatch_label.after_cancel(update_time)
        pyautogui.screenshot().save(task_folder + f"/end.png")
        with open(master_folder + "/log.csv", "a+", newline='') as file:
            csvfile = csv.writer(file, delimiter=',')
            csvfile.writerow(
                [
                    label,
                    f"{start_datehour.year}-{start_datehour.month}-{start_datehour.day}",
                    f"{start_datehour.hour}:{start_datehour.minute}:{start_datehour.second}",
                    f"{end_datehour.year}-{end_datehour.month}-{end_datehour.day}",
                    f"{end_datehour.hour}:{end_datehour.minute}:{end_datehour.second}",
                    hours,
                    minutes,
                    seconds
                ]
            )
        running = False
        button.config(text="start", height=5, width=5, command=start, font=('Arial', 30))
    hours, minutes, seconds = 0, 0, 0
    stopwatch_label.config(text='00:00:00')

def update():
    global hours, minutes, seconds
    global update_time
    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0
    if minutes == 60:
        hours += 1
        minutes = 0
    if minutes % 5 == 0 and seconds == 0:
        pyautogui.screenshot().save(task_folder + f"/{str(hours).zfill(2)}-{str(minutes).zfill(2)}-{str(seconds).zfill(2)}.png")
    stopwatch_label.config(text=f"{str(hours).zfill(2)}" + ':' + f"{str(minutes).zfill(2)}" + ':' + f"{str(seconds).zfill(2)}")
    update_time = stopwatch_label.after(1000, update)

def set_folder():
    global master_folder
    master_folder = filedialog.askdirectory()
    if master_folder:
        button.config(text="start", height=5, width=5, command=start, font=('Arial', 30))

root = tk.Tk()
root.geometry('450x70')
root.title('Freelance Clock')

stopwatch_label = tk.Label(text='00:00:00', font=('Arial', 60))
stopwatch_label.pack(side=tk.LEFT)
button = tk.Button(text='set folder', height=5, width=7, font=('Arial', 20), command=set_folder)
button.pack(side=tk.RIGHT)

root.attributes('-topmost', True)
root.resizable(0,0)
root.mainloop()