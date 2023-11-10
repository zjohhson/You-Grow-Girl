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
        if plantname == '' or plantname is None:
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">Please enter plant name.</p><br>
                    <a href="http://608dev-2.net/sandbox/sc/team07/web/lookupGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''
        if int(mintemp) >= int(maxtemp):
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">Error: minimum temperature must be strictly less than maximum temperature.</p><br>
                    <a href="http://608dev-2.net/sandbox/sc/team07/web/lookupGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''
        with open("/var/jail/home/team07/web/plants.json", "r") as read_file:
            for entry in read_file.readlines():
                try:
                    dict_string = entry[:-1]
                    entry_dict = json.loads(dict_string)
                    if entry_dict['name'].lower() == plantname.lower():
                        return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">{} already exists in JSON file.</p><br>
                        <a href="http://608dev-2.net/sandbox/sc/team07/web/lookupGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''.format(plantname)
                except json.decoder.JSONDecodeError:
                    pass
            read_file.close()
        with open("/var/jail/home/team07/web/plants.json", "a") as read_file:
            json_entry = json.dumps({"name": plantname, "watering": moisture, "light": light, "humidity": humidity, "min_temperature": mintemp, "max_temperature": maxtemp, "night_temperature": nighttemp})
            read_file.write("{}\n".format(json_entry))
            read_file.close()
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">{} entered into JSON file!</p><br>
                    <a href="http://608dev-2.net/sandbox/sc/team07/web/lookupGUI.py" style = "font-size: 20px; font-family: courier;">Back.</a></body>'''.format(plantname)

##print(request_handler({'method': 'POST', 'args': [], 'values': {}, 'content-type': 'application/x-www-form-urlencoded', 'is_json': False, 'data': b'plantname=orchid&humidity=2&moisture=2&light=2&mintemp=58&maxtemp=65&nighttemp=65', 'form': {'plantname': 'orchid', 'humidity': '2', 'moisture': '2', 'light': '2', 'mintemp': '58', 'maxtemp': '65', 'nighttemp': '65'}}))
