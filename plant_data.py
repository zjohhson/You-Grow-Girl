import sqlite3
import datetime
import numpy as np
import json
import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0,' /var/jail/home/team07/')
import traceback
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
                m_low=1400
                m_high=1400
                l_low=0
                l_high=0
                h_low=20
                h_high=20
                name_type_map = {}
                plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                for name in plant_names:
                    plant_type = c.execute("""SELECT DISTINCT plant_type FROM plant_data WHERE plant_id = ?""", (name[0],)).fetchall()
                    name_type_map[name[0]] = plant_type[0][0]
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
                        str_tot+= features2(i,temperature,light,moisture,humidity,now,optimal_values) + " | "
                    return str_tot[:-2]
                elif value == 'names':
                    return json.dumps(format_names2(name_type_map))


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
                            m_low=3510
                            m_high=3300
                        if int(optimal_values["watering"])==2:
                            m_low=3300
                            m_high=2870
                        if int(optimal_values["watering"])==3:
                            m_low=2870
                            m_high=2030
                        if int(optimal_values["watering"])==4:
                            m_low=2030
                            m_high=1400
                        if m_low >= moisture:
                            return "{}'s {}: {} and is watered".format(plant_id, value, moisture)
                        elif moisture >m_low:
                            return "{}'s {}: {} and needs to be watered".format(plant_id, value,moisture)
                    elif value == "watering":
                        if int( optimal_values["watering"])==1:
                            m_low=3510
                            m_high=3300
                        if int(optimal_values["watering"])==2:
                            m_low=3300
                            m_high=2870
                        if int(optimal_values["watering"])==3:
                            m_low=2870
                            m_high=2030
                        if int(optimal_values["watering"])==4:
                            m_low=2030
                            m_high=1400
                        return (m_low + m_high)/2
                    elif value == 'feelings':
                        
                        return features([plant_id],temperature,light,moisture,humidity,now,optimal_values)                   
                    elif value == 'temp':
                        if  6<=int(now.strftime("%H")) and int(now.strftime("%H")) <=16:
                            if int(optimal_values["min_temperature"] )<=temperature and temperature <= int(optimal_values["max_temperature"]):
                                
                                return "{}'s {}: {} and looks good".format(plant_id, value, temperature)
                            elif int(optimal_values["min_temperature"]) >temperature:
                                return "{}'s {}: {} and looks cold".format(plant_id, value, temperature)
                            else:
                                return "{}'s {}: {} and looks too warm".format(plant_id, value, temperature)
                        else:
                            if int(optimal_values["night_temperature"]) -10 <=temperature and temperature <= int(optimal_values["night_temperature"]):
                                return "{}'s {}: {} and looks good".format(plant_id, value, temperature)
                            elif int(optimal_values["night_temperature"]) -10 >temperature:
                                return "{}'s {}: {} and looks cold".format(plant_id, value, temperature)
                            else: 
                                return "{}'s {}: {} and looks too warm".format(plant_id, value, temperature)
                    elif value == 'light':
                        if 6<=int(now.strftime("%H")) and int(now.strftime("%H")) <=16:
                        
                            if int(optimal_values["light"])==1:
                                l_low=0
                                l_high=1024
                            if int(optimal_values["light"])==2:
                                l_low=1024
                                l_high=2048
                            if int(optimal_values["light"])==3:
                                l_low=2048
                                l_high=3072
                            if int(optimal_values["light"])==4:
                                l_low=3072
                                l_high=4095
                            if l_low<= light and light < l_high:
                                return "{}'s {}: {} and looks good".format(plant_id, value, light) 
                            if l_low > light:
                                return "{}'s {}: {} and looks low".format(plant_id, value, light)
                            if  light > l_high:
                                return "{}'s {}: {} and looks high".format(plant_id, value, light) 
                        else:
                            if 0<=light and light <4095:
                                return "plant is asleep"
                            else:
                                return "{}'s {}: {} but should be dark".format(plant_id, value, light)
                    elif value == 'humidity':
                        if int(optimal_values["humidity"])==1:
                            h_low=20
                            h_high=37.5
                        if int(optimal_values["humidity"])==2:
                            h_low=37.5
                            h_high=55
                        if int(optimal_values["humidity"])==3:
                            h_low=55
                            h_high=72.5
                        if int(optimal_values["humidity"])==4:
                            h_low=72.5
                            h_high=90
                        if h_low<= humidity and humidity <h_high:
                            return "{}'s {}: {} and looks good".format(plant_id, value, humidity)
                        elif humidity < h_low:
                            return "{}'s {}: {} and looks low".format(plant_id, value, humidity)
                        elif humidity > h_high:
                            return "{}'s {}: {} and looks high".format(plant_id, value, humidity)
                        return optimal_values["humidity"]
                    elif value == 'moisture':
                        if int(optimal_values["watering"])==1:
                            m_low=1400
                            m_high=2030
                        if int(optimal_values["watering"])==2:
                            m_low=2030
                            m_high=2870
                        if int(optimal_values["watering"])==3:
                            m_low=2870
                            m_high=3300
                        if int(optimal_values["watering"])==4:
                            m_low=3300
                            m_high=3510
                        if m_low<= moisture and moisture <m_high:
                            return "{}'s {}: {} and looks good".format(plant_id, value, moisture)
                        elif moisture < m_low:
                            return "{}'s {}: {} and looks low".format(plant_id, value,moisture)
                        elif moisture> m_high:
                            return "{}'s {}: {} and looks high".format(plant_id, value, moisture)
                        #return "{}'s {}: {}".format(plant_id, value, moisture)
                    elif value == 'names':
                        return json.dumps(format_names(name_type_map))
                    else:
                        return "{}'s {} does not exist in database".format(plant_id, value)
                else:
                    return "{} does not exist in database".format(plant_id)
        except Exception as e:
##            exc_type, exc_obj, exc_tb = sys.exc_info()
##            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
##            return (exc_type, fname, exc_tb.tb_lineno)
            return traceback.format_exc()
    else:
       return "Invalid Request"

def check_names(names, name):
    for name1 in names:
        if name1[0] == name:
            return True
    return False

def format_names2(name_type_map):
    length = len(name_type_map.keys())
    name_str = ""

    for name in name_type_map:
        name_str += " " + name
    
    return_dict = {}
    return_dict["plant names"] = name_str

    return return_dict

def format_names(name_type_map):
    length = len(name_type_map.keys())
    return_dict = {'plants': [], 'number_of_plants': length}
    for name in name_type_map:
        nested_dict = {"name": name, "plant_type": name_type_map[name]}
        return_dict['plants'].append(nested_dict)
    return return_dict

def features(name,temperature,light,moisture,humidity,now,optimal_values):
##    return str(optimal_values)
    m_low=1400
    m_high=1400
    l_low=0
    l_high=0
    h_low=20
    h_high=20

    if int( optimal_values["watering"])==1:
        m_low=3510
        m_high=3300
    if int(optimal_values["watering"])==2:
        m_low=3300
        m_high=2870
    if int(optimal_values["watering"])==3:
        m_low=2870
        m_high=2030
    if int(optimal_values["watering"])==4:
        m_low=2030
        m_high=1400
    if m_low>= moisture and moisture >m_high:
        m_val=1
    elif moisture > m_low:
        m_val=0
    elif moisture < m_high:
        m_val=2
                            


    if  6<=int(now.strftime("%H")) and int(now.strftime("%H")) <=16:
        if int(optimal_values["min_temperature"] )<=temperature and temperature <= int(optimal_values["max_temperature"]):
            t_val=1
                                
                                
        elif int(optimal_values["min_temperature"]) >temperature:
            t_val=0
                                
        else:
            t_val=2
                                
    else:
        if int(optimal_values["night_temperature"]) -10 <=temperature and temperature <= int(optimal_values["night_temperature"]):
            t_val=1
                                
        elif int(optimal_values["night_temperature"]) -10 >temperature:
            t_val=0
        else:
            t_val=2
                                


    if 6<=int(now.strftime("%H")) and int(now.strftime("%H")) <=16:
                        
        if int(optimal_values["light"])==1:
            l_low=0
            l_high=1024
        if int(optimal_values["light"])==2:
            l_low=1024
            l_high=2048
        if int(optimal_values["light"])==3:
            l_low=2048
            l_high=3072
        if int(optimal_values["light"])==4:
            l_low=3072
            l_high=4095
        if l_low<= light and light < l_high:
            l_val=1
        if l_low > light:
            l_val=0
        if  light > l_high:
            l_val=2 
    else:
        if 0<=light and light <4095:
            l_val=1
        else:
            l_val=0




    if int(optimal_values["humidity"])==1:
        h_low=20
        h_high=37.5
    if int(optimal_values["humidity"])==2:
        h_low=37.5
        h_high=55
    if int(optimal_values["humidity"])==3:
        h_low=55
        h_high=72.5
    if int(optimal_values["humidity"])==4:
        h_low=72.5
        h_high=90
    if h_low<= humidity and humidity <h_high:   
        h_val=1
    elif humidity < h_low:
        h_val=0
    elif humidity > h_high:
        h_val=3
    tots=[m_val,t_val, l_val, h_val]
    letters = ['M', 'T', 'L', 'H']
    names=["moisture","temp","light","humidity"]
    str1=""
    for i in range(len(tots)):
        if tots[i] != 1:
##            if len(str1) == 0:
##                str1 = str(name[0]) + ": "
##            str1 += letters[i] + ', '
            if len(str1)==0:
                str1= str(name[0]) + " is sad. " 
            if tots[i] ==0:
                str1 += str(names[i]) + " is LOW :(. "

            else:
                str1 += str(names[i]) + " is HIGH :(. "

    if len(str1)==0:
        return str(name) + " is doing good"
    else:
        return str1[:-2]
    #return m_val,t_val, l_val, h_val

def features2(name,temperature,light,moisture,humidity,now,optimal_values):
    try:
        m_low=1400
        m_high=1400
        l_low=0
        l_high=0
        h_low=20
        h_high=20

        if int( optimal_values["watering"])==1:
            m_low=3510
            m_high=3300
        if int(optimal_values["watering"])==2:
            m_low=3300
            m_high=2870
        if int(optimal_values["watering"])==3:
            m_low=2870
            m_high=2030
        if int(optimal_values["watering"])==4:
            m_low=2030
            m_high=1400
        if m_low>= moisture and moisture >m_high:
            m_val=1
        elif moisture > m_low:
            m_val=0
        elif moisture < m_high:
            m_val=2
                                


        if  6<=int(now.strftime("%H")) and int(now.strftime("%H")) <=16:
            if int(optimal_values["min_temperature"] )<=temperature and temperature <= int(optimal_values["max_temperature"]):
                t_val=1
                                    
                                    
            elif int(optimal_values["min_temperature"]) >temperature:
                t_val=0
                                    
            else:
                t_val=2
                                    
        else:
            if int(optimal_values["night_temperature"]) -10 <=temperature and temperature <= int(optimal_values["night_temperature"]):
                t_val=1
                                    
            elif int(optimal_values["night_temperature"]) -10 >temperature:
                t_val=0
            else:
                t_val=2
                                    


        if 6<=int(now.strftime("%H")) and int(now.strftime("%H")) <=16:
                            
            if int(optimal_values["light"])==1:
                l_low=0
                l_high=1024
            if int(optimal_values["light"])==2:
                l_low=1024
                l_high=2048
            if int(optimal_values["light"])==3:
                l_low=2048
                l_high=3072
            if int(optimal_values["light"])==4:
                l_low=3072
                l_high=4095
            if l_low<= light and light < l_high:
                l_val=1
            if l_low > light:
                l_val=0
            if  light > l_high:
                l_val=2 
        else:
            if 0<=light and light <4095:
                l_val=1
            else:
                l_val=0




        if int(optimal_values["humidity"])==1:
            h_low=20
            h_high=37.5
        if int(optimal_values["humidity"])==2:
            h_low=37.5
            h_high=55
        if int(optimal_values["humidity"])==3:
            h_low=55
            h_high=72.5
        if int(optimal_values["humidity"])==4:
            h_low=72.5
            h_high=90
        if h_low<= humidity and humidity <h_high:   
            h_val=1
        elif humidity < h_low:
            h_val=0
        elif humidity > h_high:
            h_val=3
        tots=[m_val,t_val, l_val, h_val]
        letters = ['M', 'T', 'L', 'H']
        names=["moisture","temp","light","humidity"]
        str1=""
        for i in range(len(tots)):
            if tots[i] != 1:
                if len(str1) == 0:
                    str1 = str(name[0]) + ": "
                str1 += letters[i] + ', '
    ##            if len(str1)==0:
    ##                str1= str(name[0]) + " is sad. " 
    ##            if tots[i] ==0:
    ##                str1 += str(names[i]) + " is LOW :(. "
    ##
    ##            else:
    ##                str1 += str(names[i]) + " is HIGH :(. "

        if len(str1)==0:
            return str(name) + " is doing good"
        else:
            return str1[:-2]
        #return m_val,t_val, l_val, h_val
    except:
        return ''
                            


import datetime
USERS = [] #update
import json
plantlist=[]
def request_handler1(request):
    if request:

        with open("/var/jail/home/team07/web/plants.json", "r") as read_file:
            for jsonObj in read_file:
                #return dict(jsonObj)
                print(jsonObj)
                data = json.loads(jsonObj)
                if data["name"]==request:
                    plantlist.append(data)
        if len(plantlist) ==0:
            with open("/var/jail/home/team07/web/plants.json", "r") as read_file:
                for jsonObj in read_file:
                    data = json.loads(jsonObj)
                    if data["name"]=="Other":
                        plantlist.append(data)
         #   return data
        return plantlist[0]
