import sys
sys.path.append('/var/jail/home/team07/web/')
import datetime
import sqlite3
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
        <h1 style="font-family:courier;"text-align:center">Enter a plant into database</h1>
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
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">Please enter plant name.</p><br><a href="http://608dev-2.net/sandbox/sc/team07/web/enterGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''
        elif plant_type == '':
            return r'''<body style="background-color:darkseagreen;"><p style = "font-size: 20px; font-family: courier;">Please enter plant type.</p><br><a href="http://608dev-2.net/sandbox/sc/team07/web/enterGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''
        else:
            now = datetime.datetime.now()
            with sqlite3.connect(plant_data_db) as c:
                c.execute("""CREATE TABLE IF NOT EXISTS plant_data (plant_id text, plant_type text, light real, humidity real, water real, temperature real, time_ timestamp);""")
                plant_names = c.execute("""SELECT DISTINCT plant_id FROM plant_data""").fetchall()
                if check_names(plant_names, plant_name):
                    return r'''<body style="background-color:darkseagreen;"><div style = "font-size: 20px; font-family: courier;">{}
                            already exists in database.</div><br><a href="http://608dev-2.net/sandbox/sc/team07/web/enterGUI.py" style = "font-size: 20px; font-family: courier;">Back</a></body>'''.format(plant_name)
                else:
                    c.execute("""INSERT INTO plant_data VALUES (?,?,?,?,?,?,?);""", (plant_name, plant_type, 0, 0, 0, 0, now,))
                    return r'''<body style="background-color:darkseagreen;"><div style = "font-size: 20px; font-family: courier;">{}
                        the {} entered into database!</div><br><a href="http://608dev-2.net/sandbox/sc/team07/web/enterGUI.py" style = "font-size: 20px; font-family: courier;">Click here to submit another plant.</a></body>'''.format(plant_name, plant_type)
