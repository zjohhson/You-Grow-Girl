import sys
sys.path.append('/var/jail/home/team07/web/')
import webscraper

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
        <h1 style="font-family:courier;"text-align:center">Enter plant metrics.</h1>
        <form action="http://608dev-2.net/sandbox/sc/team07/json_editor.py" method="post">
          <label for="plantname" style="font-family:courier;">Common plant name (e.g. basil, orchid):</label><br>
          <input type="text" id="plantname" name="plantname">
          <br>
          <br>
          <label for="temperature" style="font-family:courier;">Temperature:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" value="2" min="0" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <br>
          <label for="humidity" style="font-family:courier;">Humidity:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" value="2" min="0" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <br>
          <label for="moisture" style="font-family:courier;">Moisture:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" value="2" min="0" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <br>
          <label for="light" style="font-family:courier;">Light:</label><br>
          <div class="slidecontainer" style="font-family:courier;">
            <input type="range" value="2" min="0" max="4" oninput="this.nextElementSibling.value = this.value">
            <output>2</output>
          </div>
          <br>
          <input type="submit">
          <br>
          <br>
          <a href="http://608dev-2.net/sandbox/sc/team07/web/lookupGUI.py" style = "font-size: 20px; font-family: courier;">Back</a>

        </form>

        </body>
        </html>
        '''.replace('## text ##', text)
