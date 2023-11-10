import sqlite3
plant_data_db = '/var/jail/home/team07/plant_data.db'
##conn = sqlite3.connect(plant_data_db)
##c = conn.cursor()

##c.execute("""SELECT * FROM plant_data;""")
##c.execute("""DELETE FROM plant_data WHERE moisture = (?);""", 0.0)
##print("we have deleted", c.rowcount, "records")
##conn.commit()
##conn.close()

def request_handler(request):
    if request["method"] == 'GET':
	with sqlite3.connect(plant_data_db) as c:
	    c.execute('''DELETE FROM plant_data WHERE moisture = (?);''', 0.0)
	    return "we have deleted" + str(c.rowcount) + "records"
