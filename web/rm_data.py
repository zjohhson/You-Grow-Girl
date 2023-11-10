import sqlite3
plant_data_db = '/var/jail/home/team07/plant_data.db'

def request_handler(request):
    if request["method"] == 'GET':
        with sqlite3.connect(plant_data_db) as c:
            c.execute('''DELETE FROM plant_data WHERE moisture = (?);''', 0.0)
            return "we have deleted" + str(c.rowcount) + "records"
