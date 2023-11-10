import sys
sys.path.append('/var/jail/home/team07/web/')
import sqlite3
import datetime
import plant_data_grapher2

##plant_data_db = '/Users/zachjohnson/Desktop/plant_data.db'
plant_data_db = '/var/jail/home/team07/plant_data.db'

def check_names(names, name):
    for name1 in names:
        if name1[0] == name:
            return True
    return False

def request_handler(request):
    if request['method'] == 'GET':
        return r'''<!DOCTYPE html>
        <html>
        <body style="background-color:powderblue;">
        <h1 style="font-family:verdana;"text-align:center">Enter a plant.</h1>
        <form action="" method="post">
          <label for="plantname">Plant name:</label><br>
          <input type="text" id="plantname" name="plantname">
          <br>
          <label for="planttype">Plant type:</label><br>
          <input type="text" id="planttype" name="planttype">
          <br>
          <input type="submit">
        <br>
        <br>
        <br>
        <h1>See analytics on an existing plant.</h1>
        <form action="" method="post">
          <label for="plantname_analytics">Plant name:</label><br>
          <input type="text" id="plantname_analytics" name="plantname_analytics">
          <br>
          <label for="planttype_analytics">Plant type:</label><br>
          <input type="text" id="planttype_analytics" name="planttype_analytics">
          <br>
          <input type="submit">
        <br>
        <br>
        <a href="lookupGUI.py">Look up/enter a plant.</a>

        </form>

        </body>
        </html>
        '''
    elif request['method'] == 'POST':
        plant_name = request['form']['plantname']
        plant_type = request['form']['planttype']
        plant_name_analytics = request['form']['plantname_analytics']
        plant_type_analytics = request['form']['planttype_analytics']
        if ((plant_name != '' or plant_type != '') and (plant_name_analytics == '' and plant_type_analytics == '')):
            if plant_name == '':
                return "please enter plant name"
            elif plant_type == '':
                return 'please enter plant type'
            else:
                now = datetime.datetime.now()
                with sqlite3.connect(plant_data_db) as c:
                    c.execute("""CREATE TABLE IF NOT EXISTS plant_data (plant_id text, plant_type text, light real, humidity real, water real, temperature real, time_ timestamp);""")
                    plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                    if check_names(plant_names, plant_name):
                        return r'''<div>{} already exists in database.</div><br><a href="http://608dev-2.net/sandbox/sc/team07/testGUI.py">Click here to submit another plant.</a>'''.format(plant_name)
                    else:
                        c.execute("""INSERT INTO plant_data VALUES (?,?,?,?,?,?,?);""", (plant_name, plant_type, 0, 0, 0, 0, now,))
                        return r'''<div>{} the {} entered into database!</div><br><a href="http://608dev-2.net/sandbox/sc/team07/testGUI.py">Click here to submit another plant.</a>'''.format(plant_name, plant_type)
        elif ((plant_name == '' and plant_type == '') and (plant_name_analytics != '' or plant_type_analytics != '')):
##            if plant_name_analytics == '' and plant_type_analytics == '':
##                return 'please enter plant type and plant name'
            if plant_name_analytics == '':
                return "please enter plant name"
            elif plant_type_analytics == '':
                return 'please enter plant type'
            else:
                with sqlite3.connect(plant_data_db) as c:
                    plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                    if not check_names(plant_names, plant_name_analytics):
                        return "{} does not exist in database.".format(plant_name_analytics)
                    most_recent = c.execute("""SELECT * FROM plant_data WHERE plant_id = (?) ORDER BY ROWID DESC LIMIT 1;""", (plant_name_analytics,)).fetchall()[0]
                    plant_type = most_recent[1]
                    if plant_type != plant_type_analytics:
                        return "{} exists in database, but is actually a {}, not a {}.".format(plant_name_analytics, plant_type, plant_type_analytics)
                    else:
                        request2 = {'method': 'GET', 'args': [], 'values': {'id': plant_name_analytics, 'esp': 'false', 'plant_type': plant_type_analytics}, 'content-type': 'application/x-www-form-urlencoded',
                            'is_json': False} #, 'data': b'plantname=&planttype=&plantname=&planttype=', 'form': {'plantname': '', 'planttype': ''}}
                        return plant_data_grapher2.request_handler(request2)
        else:
            return 'Error in processing your request :( please make sure you are submitting a request to either enter a plant or see analytics, but not both!'
