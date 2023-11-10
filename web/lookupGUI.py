import sys
sys.path.append('/var/jail/home/team07/web/')
import webscraper

guide1 = 'Enter your plant ranges below. For humidity, light, and moisture, you will choose a value on a 4 point scale, where: \n '
guide2 = 'Humidity: \n 1 = requires low humidity (20-38%) \n 2 = requires medium-low humidity (38-55%) \n 3 (default) = requires medium humidity (55-73%) \n 4 = requires high humidity (73-90%)\n'
guide3 = 'Light: \n 1 = requires low light (x-x lumens) \n 2 = requires medium-low light (x-x lumens) \n 3 (default) = requires medium light (x-x lumens) \n 4 = requires high light (x-x lumens)\n'
guide4 = 'Moisture: \n 1 = requires low moisture (0-30%) \n 2 = requires medium-low moisture (30-70%) \n 3 (default) = requires medium moisture (70-90%) \n 4 = requires high moisture (90-100%)\n'
guide5 = 'Temperature: choose the optimal temperature range for your plant (measured in degrees Fahrenheit). Minimum temperature must be < maximum temperature.'

def request_handler(request):
    if request['method'] == 'GET':
        return r'''<!DOCTYPE html>
        <html>
        <body style="background-color:darkseagreen;">
        <h1 style="font-family:courier;"text-align:center">Look up a plant.</h1>
        <form action="" method="post">
          <label for="scientific name" style="font-family:courier;">Scientific name of plant:</label><br>
          <input type="text" id="scientific name" name="scientific name">
          <br>
          <input type="submit">
          <br>
          <br>
          <br>
          <a href="http://608dev-2.net/sandbox/sc/team07/web/GUI.py" style = "font-size: 20px; font-family: courier;">Back to main page</a>
        </form>

        </body>
        </html>
        '''

    elif request['method'] == 'POST':
        scientific_name = request['form']['scientific name']
        request = {'method': 'GET', 'values': {'topic': scientific_name, 'len': 1}}
        text = webscraper.request_handler(request)
        text = text.lstrip()
        return r'''<!DOCTYPE html>
        <html>
        <body style="background-color:darkseagreen;">
        <p style="font-family:courier; font-style:italic;">## text ##</p>
        <br>
        <br>
        <p style="font-family:courier; font-weight:bold;">## guide1 ##</p>
        <p style="font-family:courier; font-weight:bold;">## guide2 ##</p>
        <p style="font-family:courier; font-weight:bold;">## guide3 ##</p>
        <p style="font-family:courier; font-weight:bold;">## guide4 ##</p>
        <p style="font-family:courier; font-weight:bold;">## guide5 ##</p>
        <h1 style="font-family:courier;"text-align:center">Enter plant metrics.</h1>
        <form action="http://608dev-2.net/sandbox/sc/team07/web/json_editor.py" method="post">
          <label for="plantname" style="font-family:courier;">Common plant name (e.g. basil, orchid):</label><br>
          <input type="text" id="plantname" name="plantname">
          <br>
          <br>
          <label for="humidity" style="font-family:courier;">Humidity:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" id = "humidity" name = "humidity" value="2" min="1" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <br>
          <label for="moisture" style="font-family:courier;">Moisture:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" id = "moisture" name = "moisture" value="2" min="1" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <br>
          <label for="light" style="font-family:courier;">Light:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" id = "light" name = "light" value="2" min="1" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <br>
          <label for="min temperature" style="font-family:courier;">Minimum temperature:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" id = "mintemp" name = "mintemp" value="65" min="50" max="85" oninput="this.nextElementSibling.value = this.value">
            <output>65</output>
          </div>
          <br>
          <br>
          <label for="max temperature" style="font-family:courier;">Maximum temperature:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" id = "maxtemp" name = "maxtemp" value="65" min="50" max="85" oninput="this.nextElementSibling.value = this.value">
            <output>65</output>
          </div>
          <br>
          <br>
          <label for="night temperature" style="font-family:courier;">Night temperature:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" id = "nighttemp" name = "nighttemp" value="65" min="50" max="85" oninput="this.nextElementSibling.value = this.value">
            <output>65</output>
          </div>
          <br>
          <br>
          <input type="submit">
          <br>
          <br>
          <a href="http://608dev-2.net/sandbox/sc/team07/web/lookupGUI.py" style = "font-size: 20px; font-family: courier;">Back</a>

        </form>

        </body>
        </html>
        '''.replace('## text ##', text).replace('## guide1 ##', guide1).replace('## guide2 ##', guide2).replace('## guide3 ##', guide3).replace('## guide4 ##', guide4).replace('## guide5 ##', guide5)
