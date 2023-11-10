import sqlite3
import datetime
import numpy as np
import json
import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0,' /var/jail/home/team07/')
#import finaljson

##plant_data_db = '/var/jail/home/zjohnson/final_project/plant_data.db'
##plant_data_db = '/Users/zachjohnson/Desktop/plant_data.db'
plant_data_db = '/var/jail/home/team07/plant_data.db'

def request_handler(request):
    if request["method"] == "POST":
        plant_id = request["form"]["plant_id"]
        plant_type = request["form"]["plant_type"]
        light = float(request["form"]["light"])
        humidity = float(request["form"]["humidity"])
        temperature = float(request["form"]["temp"])
        moisture = float(request["form"]["moisture"])
        now = datetime.datetime.now()
        with sqlite3.connect(plant_data_db) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS plant_data (plant_id text, plant_type text, light real, humidity real, moisture real, temperature real, time_ timestamp);""")
            c.execute("""INSERT INTO plant_data VALUES (?,?,?,?,?,?,?);""", (plant_id, plant_type, light, humidity, moisture, temperature, now,))
            return "Data posted successfully!"

    elif request["method"] == "GET":
        try:
            with sqlite3.connect(plant_data_db) as c:
                m_low=0
                m_high=0
                l_low=0
                l_high=0
                h_low=0
                h_high=0
                plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                plant_id = request['values']['plant_id']
                value = request["values"]["value"]
                if (value == 'notification'):
                    str_tot=""
                    for i in plant_names:
                        most_recent = c.execute("""SELECT * FROM plant_data WHERE plant_id = (?) ORDER BY ROWID DESC LIMIT 1;""", (i[0],)).fetchall()[0]
                        plant_type = most_recent[1]
                        light = most_recent[2]
                        humidity = most_recent[3]
                        moisture = most_recent[4]
                        temperature = most_recent[5]
                        now= datetime.datetime.now()
                        optimal_values = request_handler1(plant_type)
                        str_tot+= features(i,temperature,light,moisture,humidity,now,optimal_values) + " "
                    return str_tot
                #else:
                    #return "{} is not a plant.".format(plant_id)
                if check_names(plant_names, plant_id):
                    most_recent = c.execute("""SELECT * FROM plant_data WHERE plant_id = (?) ORDER BY ROWID DESC LIMIT 1;""", (plant_id,)).fetchall()[0]
                    plant_type = most_recent[1]
                    light = most_recent[2]
                    humidity = most_recent[3]
                    moisture = most_recent[4]
                    temperature = most_recent[5]
                    now= datetime.datetime.now()
                    optimal_values = request_handler1(plant_type) # nitya
                    
                    if value == 'water':
                        ## replace with code that checks for thresholds
                        #return "{} is doing well!".format(plant_id)
                        if int( optimal_values["watering"])==1:
                            m_low=0
                            m_high=3
                        if int(optimal_values["watering"])==2:
                            m_low=3
                            m_high=6
                        if int(optimal_values["watering"])==3:
                            m_low=7
                            m_high=9
                        if int(optimal_values["watering"])==4:
                            m_low=9
                            m_high=10
                        if m_low<= moisture:
                            return "{}'s {}: {} and is watered".format(plant_id, value, moisture)
                        elif moisture < m_low:
                            return "{}'s {}: {} and needs to be watered".format(plant_id, value,moisture)
                    elif value == 'feelings':
                        
                        return features([plant_id],temperature,light,moisture,humidity,now,optimal_values)                   
                    elif value == 'temp':
                        if  6<=int(now.strftime("%H"))<=16:
                            if int(optimal_values["min_temperature"] )<=temperature <= int(optimal_values["max_temperature"]):
                                
                                return "{}'s {}: {} and looks good".format(plant_id, value, temperature)
                            elif int(optimal_values["min_temperature"]) >temperature:
                                return "{}'s {}: {} and looks cold".format(plant_id, value, temperature)
                            else:
                                return "{}'s {}: {} and looks too warm".format(plant_id, value, temperature)
                        else:
                            if int(optimal_values["night_temperature"]) -10 <=temperature <= int(optimal_values["night_temperature"]):
                                return "{}'s {}: {} and looks good".format(plant_id, value, temperature)
                            elif int(optimal_values["night_temperature"]) -10 >temperature:
                                return "{}'s {}: {} and looks cold".format(plant_id, value, temperature)
                            else: 
                                return "{}'s {}: {} and looks too warm".format(plant_id, value, temperature)
                    elif value == 'light':
                        if 6<=int(now.strftime("%H"))<=16:
                        
                            if int(optimal_values["light"])==1:
                                l_low=20
                                l_high=40
                            if int(optimal_values["light"])==2:
                                l_low=40
                                l_high=60
                            if int(optimal_values["light"])==3:
                                l_low=60
                                l_high=80
                            if int(optimal_values["light"])==4:
                                l_low=80
                                l_high=100
                            if l_low<= light < l_high:
                                return "{}'s {}: {} and looks good".format(plant_id, value, light) 
                            if l_low > light:
                                return "{}'s {}: {} and looks low".format(plant_id, value, light)
                            if  light > l_high:
                                return "{}'s {}: {} and looks high".format(plant_id, value, light) 
                        else:
                            if 0<=light<10:
                                return "plant is asleep"
                            else:
                                return "{}'s {}: {} but should be dark".format(plant_id, value, light)
                    elif value == 'humidity':
                        if int(optimal_values["humidity"])==1:
                            h_low=20
                            h_high=40
                        if int(optimal_values["humidity"])==2:
                            h_low=40
                            h_high=60
                        if int(optimal_values["humidity"])==3:
                            h_low=60
                            h_high=80
                        if int(optimal_values["humidity"])==4:
                            h_low=80
                            h_high=100
                        if h_low<= humidity <h_high:
                            return "{}'s {}: {} and looks good".format(plant_id, value, humidity)
                        elif humidity < h_low:
                            return "{}'s {}: {} and looks low".format(plant_id, value, humidity)
                        elif humidity > h_high:
                            return "{}'s {}: {} and looks high".format(plant_id, value, humidity)
                        return optimal_values["humidity"]
                    elif value == 'moisture':
                        if int(optimal_values["watering"])==1:
                            m_low=0
                            m_high=3
                        if int(optimal_values["watering"])==2:
                            m_low=3
                            m_high=6
                        if int(optimal_values["watering"])==3:
                            m_low=7
                            m_high=9
                        if int(optimal_values["watering"])==4:
                            m_low=9
                            m_high=10
                        if m_low<= moisture <m_high:
                            return "{}'s {}: {} and looks good".format(plant_id, value, moisture)
                        elif moisture < m_low:
                            return "{}'s {}: {} and looks low".format(plant_id, value,moisture)
                        elif moisture> m_high:
                            return "{}'s {}: {} and looks high".format(plant_id, value, moisture)
                        #return "{}'s {}: {}".format(plant_id, value, moisture)
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


def features(name,temperature,light,moisture,humidity,now,optimal_values):
    m_low=0
    m_high=0
    l_low=0
    l_high=0
    h_low=0
    h_high=0

    if int( optimal_values["watering"])==1:
        m_low=0
        m_high=3
    if int(optimal_values["watering"])==2:
        m_low=3
        m_high=6
    if int(optimal_values["watering"])==3:
        m_low=7
        m_high=9
    if int(optimal_values["watering"])==4:
        m_low=9
        m_high=10
    if m_low<= moisture <m_high:
        m_val=1
    elif moisture < m_low:
        m_val=0
    elif moisture> m_high:
        m_val=2
                            


    if  6<=int(now.strftime("%H"))<=16:
        if int(optimal_values["min_temperature"] )<=temperature <= int(optimal_values["max_temperature"]):
            t_val=1
                                
                                
        elif int(optimal_values["min_temperature"]) >temperature:
            t_val=0
                                
        else:
            t_val=2
                                
    else:
        if int(optimal_values["night_temperature"]) -10 <=temperature <= int(optimal_values["night_temperature"]):
            t_val=1
                                
        elif int(optimal_values["night_temperature"]) -10 >temperature:
            t_val=0
        else:
            t_val=2
                                


    if 6<=int(now.strftime("%H"))<=16:
                        
        if int(optimal_values["light"])==1:
            l_low=20
            l_high=40
        if int(optimal_values["light"])==2:
            l_low=40
            l_high=60
        if int(optimal_values["light"])==3:
            l_low=60
            l_high=80
        if int(optimal_values["light"])==4:
            l_low=80
            l_high=100
        if l_low<= light < l_high:
            l_val=1
        if l_low > light:
            l_val=0
        if  light > l_high:
            l_val=2 
    else:
        if 0<=light<10:
            l_val=1
        else:
            l_val=0




    if int(optimal_values["humidity"])==1:
        h_low=20
        h_high=40
    if int(optimal_values["humidity"])==2:
        h_low=40
        h_high=60
    if int(optimal_values["humidity"])==3:
        h_low=60
        h_high=80
    if int(optimal_values["humidity"])==4:
        h_low=80
        h_high=100
    if h_low<= humidity <h_high:   
        h_val=1
    elif humidity < h_low:
        h_val=0
    elif humidity > h_high:
        h_val=3
    tots=[m_val,t_val, l_val, h_val]
    names=["moisture","temp","light","humidity"]
    str1=""
    for i in range(len(tots)):
        if tots[i] != 1:
            if len(str1)==0:
                str1= str(name[0]) + " is sad. " 
            if tots[i] ==0:
                str1 += str(names[i]) + " is LOW :(. "

            else:
                str1 += str(names[i]) + " is HIGH :(. "

    if len(str1)==0:
        return str(name) + " is doing good"
    else:
        return str1
    #return m_val,t_val, l_val, h_val
                            


import datetime
USERS = [] #update
import json
plantlist=[]
def request_handler1(request):
    if request:

        with open("/var/jail/home/team07/plants.json", "r") as read_file:
            for jsonObj in read_file:
                #return dict(jsonObj)
                print(jsonObj)
                data = json.loads(jsonObj)
                if data["name"]==request:
                    plantlist.append(data)
        if len(plantlist) ==0:
            data = json.loads(jsonObj)
            return data
        return plantlist
