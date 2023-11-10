import tkinter as tk
import sqlite3
import datetime
import numpy as np

plant_data_db = '/Users/zachjohnson/Desktop/plant_data.db'
##plant_data_db = '/var/jail/home/team07/plant_data.db'

HEIGHT = 700
WIDTH = 800

def check_names(names, name):
    for name1 in names:
        if name1[0] == name:
            return True
    return False

def upload_plant(entry1, entry2):
    if entry1.get() == '' and entry2.get() == '':
        return_label["text"] = 'please enter plant type and plant name'
    elif entry1.get() == '':
        return_label["text"] = "please enter plant name"
    elif entry2.get() == '':
        return_label["text"] = 'please enter plant type'
    else:
        now = datetime.datetime.now()
        plant_name = entry1.get()
        plant_type = entry2.get()
        with sqlite3.connect(plant_data_db) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS plant_data (plant_id text, plant_type text, light real, humidity real, water real, temperature real, time_ timestamp);""")
            plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
            if check_names(plant_names, plant_name):
                return_label["text"] = "{} already exists in database.".format(plant_name)
                print("{} already exists in database.".format(plant_name))
            else:
                c.execute("""INSERT INTO plant_data VALUES (?,?,?,?,?,?,?);""", (plant_name, plant_type, 0, 0, 0, 0, now,))
                return_label["text"] = "{} the {} entered into database!".format(plant_name, plant_type)
                print("{} the {} entered into database!".format(plant_name, plant_type))

def get_plant_type(plant_type):
    print(plant_type)

root = tk.Tk()

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.grid()

frame = tk.Frame(root, bg = '#C0E7C4')
frame.place(relwidth = 1, relheight = 1)

button1 = tk.Button(root, highlightbackground = 'white', text = "Submit!", fg = 'black', font = 40, command=lambda: upload_plant(entry1, entry2))
button1.place(relx = 0.4, rely = 0.075, relwidth = 0.1, relheight = 0.05)

label1 = tk.Label(frame, text="Enter plant name:", bg = '#C0E7C4', font = 40)
label1.place(relx = 0, rely = 0.075, relwidth = 0.15, relheight = 0.05)

entry1 = tk.Entry(frame, bg = 'white', font = 40)
entry1.place(relx = 0.15, rely = 0.075, relwidth = 0.25, relheight = 0.05)

##button2 = tk.Button(root, highlightbackground = 'white', text = "Submit!", fg = 'black', font = 40, command=lambda: get_plant_type(entry2.get()))
##button2.place(relx = 0.4, rely = 0.175, relwidth = 0.1, relheight = 0.05)

label2 = tk.Label(frame, text="Enter plant type:", bg = '#C0E7C4', font = 40)
label2.place(relx = 0, rely = 0.175, relwidth = 0.15, relheight = 0.05)

return_label = tk.Label(frame, bg = '#C0E7C4', font = 40)
return_label.place(relx = 0.3, rely = 0.475, relwidth = 0.4, relheight = 0.05)

entry2 = tk.Entry(frame, bg = 'white', font = 40)
entry2.place(relx = 0.15, rely = 0.175, relwidth = 0.25, relheight = 0.05)

root.mainloop()
