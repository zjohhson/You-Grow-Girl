import sqlite3
import datetime
import numpy as np
import json
##import finaljson

##plant_data_db = '/var/jail/home/zjohnson/final_project/plant_data.db'
plant_data_db = '/Users/zachjohnson/Desktop/plant_data.db'
##plant_data_db = '/var/jail/home/team07/plant_data.db'

def request_handler(request):
    if request["method"] == "POST":
        plant_id = request["values"]["plant_id"]
        plant_type = request["values"]["plant_type"]
        light = float(request["values"]["light"])
        humidity = float(request["values"]["humidity"])
        temperature = float(request["values"]["temp"])
        moisture = float(request["values"]["moisture"])
        now = datetime.datetime.now()
        with sqlite3.connect(plant_data_db) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS plant_data (plant_id text, plant_type text, light real, humidity real, moisture real, temperature real, time_ timestamp);""")
            c.execute("""INSERT INTO plant_data VALUES (?,?,?,?,?,?,?);""", (plant_id, plant_type, light, humidity, moisture, temperature, now,))
            return "Data posted successfully!"

    elif request["method"] == "GET":
        try:
            with sqlite3.connect(plant_data_db) as c:
                name_type_map = {}
                plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                for name in plant_names:
                    plant_type = c.execute("""SELECT DISTINCT plant_type FROM plant_data WHERE plant_id = (?);""", (name,)).fetchall()
                return plant_type
                plant_id = request['values']['plant_id']
                value = request["values"]["value"]
                if check_names(plant_names, plant_id):
                    most_recent = c.execute("""SELECT * FROM plant_data WHERE plant_id = (?) ORDER BY ROWID DESC LIMIT 1;""", (plant_id,)).fetchall()[0]
                    plant_type = most_recent[1]
                    light = most_recent[2]
                    humidity = most_recent[3]
                    moisture = most_recent[4]
                    temperature = most_recent[5]
                    optimal_values = finaljson.request_handler(plant_type) # nitya
                    if value == 'feelings':
                        ## replace with code that checks for thresholds
                        return "{} is doing well!".format(plant_id)
                    elif value == 'water':
                        return "{} needs to be watered.".format(plant_id)
                    elif value == 'notification':
                        return "{} is a plant.".format(plant_id)
                    elif value == 'temp':
                        return "{}'s {}: {}".format(plant_id, value, temperature)
                    elif value == 'light':
                        return "{}'s {}: {}".format(plant_id, value, light)
                    elif value == 'humidity':
                        return "{}'s {}: {}".format(plant_id, value, humidity)
                    elif value == 'moisture':
                        return "{}'s {}: {}".format(plant_id, value, moisture)
                    elif value == 'names':
                        return json.dumps(format_names(plant_names))
                    else:
                        return "{}'s {} does not exist in database".format(plant_id, value)
                else:
                    return "{} does not exist in database".format(plant_id)
        except Exception as e:
            return e
    else:
       return "Invalid Request"

def check_names(names, name):
    for name1 in names:
        if name1[0] == name:
            return True
    return False

def format_names(plant_names):
    length = len(plant_names)
    return_dict = {'plants': [], 'number_of_plants': len(plant_names)}
    for name in plant_names:
        nested_dict = {"name": name}
        return_dict['plants'].append(nested_dict)
    return return_dict

