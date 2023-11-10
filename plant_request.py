fake_data = {"alice": [77, 3, 30, 20, "low water level"], \
 "bob": [95, 2, 10, 20, "high water level"], \
 "carol": [82, 6, 100, 90, "perfect water level"]}

 # index 0 - temp, 1 - moisture, 2 - illumination, 3 - humidity, 4 - water level

def request_handler(request):
    if request['method'] == "GET":
        # replace this functionality with database
        plant_id = request["values"]["plant_id"]
        data = request["values"]["value"]

        # handle different data
        resp = "nothing"

        if data == "notification":
            return "This is the status of all of your plants!"

        if data == "temp":
            resp = fake_data[plant_id][0]
        elif data == "moisture":
            resp = fake_data[plant_id][1]
        elif data == "light":
            resp = fake_data[plant_id][2]
        elif data == "humidity":
            resp = fake_data[plant_id][3]
        elif data == "water":
            resp = fake_data[plant_id][4]
        elif data == "feelings": # get general health level
            resp = get_health(plant_id)
            
        resp = plant_id + ": " + resp
        return resp

    else:
      return "Unable to process your request"

def get_health(plant_id):
    # check all plant data and return plant needs
    return "Feeling great!"
