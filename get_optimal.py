import datetime
USERS = [] #update
import json
plantlist=[]
def request_handler(request):
    if request:
        with open("/var/jail/home/team07/web/plants.json", "r") as read_file:
            for jsonObj in read_file:
                #return dict(jsonObj)
                print(jsonObj)
                data = json.loads(jsonObj)
                if data["name"]==request['values']['name']:
                    plantlist.append(data)
        if len(plantlist) ==0:
            with open("/var/jail/home/team07/web/plants.json", "r") as read_file:
                for jsonObj in read_file:
                    data = json.loads(jsonObj)
                    if data["name"]=="Other":
                        plantlist.append(data)
         #   return data
        return plantlist[0]["light"]

