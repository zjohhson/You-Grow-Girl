import sqlite3
import datetime
USERS = [] #update
import json
plantlist=[]
def request_handler(request):
    if request['method'] == 'POST':
        plantname = request['form']['plantname']
        mintemp = request['form']['mintemp']
        maxtemp = request['form']['maxtemp']
        nighttemp = request['form']['nighttemp']
        humidity = request['form']['humidity']
        light = request['form']['light']
        moisture = request['form']['moisture']
        with open("/var/jail/home/team07/web/plants.json", "a") as read_file:
            return [plantname, mintemp, maxtemp, nighttemp, humidity, light, moisture]
##            json_string = '{\"name\": \"{}\", \"watering\": \"{\"}, \"light\": \"{}\", \"humidity\": \"{}\", \"min_temperature\": \"{}\", \"max_temperature\": \"{}\", \"night_temperature\": \"{}\"}'.format(plantname,
##                moisture, light, humidity, mintemp, maxtemp, nighttemp)
            return json_string
##            read_file.write("/nJSONSTUFF")
##            read_file.close()
