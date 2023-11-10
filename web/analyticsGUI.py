import sys
sys.path.append('/var/jail/home/team07/web/')
import sqlite3
import datetime
import plant_data_grapher2
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
        <body style="background-color:darkseagreen;">
        <h1 style="font-family:courier;"text-align:center">See analytics on a plant</h1>
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
        <a href="GUI.py" style = "font-size: 20px; font-family: courier;">Back to main page.</a>
        </form>

        </body>
        </html>
        '''
    elif request['method'] == 'POST':
        plant_name = request['form']['plantname']
        plant_type = request['form']['planttype']
        if plant_name == '':
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">Please enter plant name.</p><br>
                    <a href="http://608dev-2.net/sandbox/sc/team07/web/analyticsGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''
        elif plant_type == '':
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">Please enter plant type.</p><br>
                    <a href="http://608dev-2.net/sandbox/sc/team07/web/analyticsGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''
        else:
            with sqlite3.connect(plant_data_db) as c:
                plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                if not check_names(plant_names, plant_name):
                    return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">{} does not exist in database.</p><br>
                            <a href="http://608dev-2.net/sandbox/sc/team07/web/analyticsGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''.format(plant_name)
                most_recent = c.execute("""SELECT * FROM plant_data WHERE plant_id = (?) ORDER BY ROWID DESC LIMIT 1;""", (plant_name,)).fetchall()[0]
                plant_type1 = most_recent[1]
                if plant_type != plant_type:
                    return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">{} exists in database, but is actually a {}, not a {}.</p><br>
                            <a href="http://608dev-2.net/sandbox/sc/team07/web/analyticsGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''.format(plant_name, plant_type1, plant_type)
                else:
                    request2 = {'method': 'GET', 'args': [], 'values': {'id': plant_name, 'esp': 'false', 'plant_type': plant_type}, 'content-type': 'application/x-www-form-urlencoded',
                        'is_json': False} #, 'data': b'plantname=&planttype=&plantname=&planttype=', 'form': {'plantname': '', 'planttype': ''}}
                    return plant_data_grapher2.request_handler(request2)
