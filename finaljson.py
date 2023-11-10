import sqlite3
import datetime
USERS = [] #update
import json
plantlist=[]
def request_handler(request):
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
