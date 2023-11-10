import sqlite3
import datetime
import numpy as np
import json
import finaljson

##plant_data_db = '/var/jail/home/zjohnson/final_project/plant_data.db'
##plant_data_db = '/Users/zachjohnson/Desktop/plant_data.db'
lant_data_db = '/var/jail/home/team07/plant_data.db'

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
                plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                plant_id = request['values']['plant_id']
                value = request["values"]["value"]
                if check_names(plant_names, plant_id):
                    most_recent = c.execute("""SELECT * FROM plant_data WHERE plant_id = (?) ORDER BY ROWID DESC LIMIT 1;""", (plant_id,)).fetchall()[0]
                    plant_type = most_recent[1]
                    light = most_recent[2]
                    humidity = most_recent[3]
                    moisture = most_recent[4]
                    temperature = most_recent[5]
                    now= datetime.datetime.now()
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
                    # elif value == 'light':
                        # if now { within time }:
                        
                            # if optimal_values["light"]==1:
                                # h_low=20
                                # h_high=40
                            # if optimal_values["light"]==2:
                                # h_low=40
                                # h_high=60
                            # if optimal_values["light"]==3:
                                # h_low=60
                                # h_high=80
                            # if optimal_values["light"]==4:
                                # h_low=80
                                # h_high=100
                        # else:
                            # if 0<light<10:
                                # return "plant is asleep"
                            # else:
                                # return "{}'s {}: {} but should be dark".format(plant_id, value, light)
                    elif value == 'humidity':
                        if optimal_values["humidity"]==1:
                            h_low=20
                            h_high=40
                        if optimal_values["humidity"]==2:
                            h_low=40
                            h_high=60
                        if optimal_values["humidity"]==3:
                            h_low=60
                            h_high=80
                        if optimal_values["humidity"]==4:
                            h_low=80
                            h_high=100
                        if h_low<= humidity <h_high:
                            return "{}'s {}: {} and looks good".format(plant_id, value, humidity)
                        elif humidty < h_low:
                            return "{}'s {}: {} and looks low".format(plant_id, value, humidity)
                        elif humidty > h_high:
                            return "{}'s {}: {} and looks highc".format(plant_id, value, humidity)
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

