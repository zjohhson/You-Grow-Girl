from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import output_file, show
from bokeh.layouts import row
import datetime
import sqlite3


plant_data_db = '/var/jail/home/team07/plant_data.db'

def request_handler(request):
    if request['method'] == "GET":
        id = request["values"]["id"]
        plant_type = request["values"]["plant_type"]
        one_day_ago = datetime.datetime.now() - datetime.timedelta(seconds = 60*60*24)
        if request["values"]["esp"] == "true":
            kind = request["values"]["data_type"]
            with sqlite3.connect(plant_data_db) as c:
                result = []
                data = c.execute("""SELECT * FROM plant_data WHERE plant_id = ? AND plant_type = ? AND time_ > ? ORDER BY time_ DESC;""", (id, plant_type, one_day_ago)).fetchall()
                if (kind == 'light'):
                    index = 2
                elif (kind == 'humidity'):
                    index = 3
                elif (kind == 'water'):
                    index = 4
                elif (kind == 'temperature'):
                    index = 5
                else:
                    return "invalid type of measurement :("
                for i in range(48):
                    try:
                        result.append(data[i][index])
                    except:
                        continue
                result.reverse()
                return result

        with sqlite3.connect(plant_data_db) as c:
            data = c.execute("""SELECT * FROM plant_data WHERE plant_id = ? AND plant_type = ? AND time_ > ? ORDER BY time_ ASC;""", (id, plant_type, one_day_ago)).fetchall()
            light = [elem[2] for elem in data]
            for i in range(len(light)):
                light[i] = light[i]/4096 * 100
            times = [datetime.datetime.strptime(elem[6],'%Y-%m-%d %H:%M:%S.%f') for elem in data]
            light_figure = figure(x_axis_type="datetime", plot_height = 300, y_range = (0,100))
            light_figure.line(times, light, legend_label = id + " light (%)", line_width = 4, color = 'yellow')

            light_figure.xaxis.axis_label = "Time"
            light_figure.yaxis.axis_label = "Light (%)"

            humidity = [elem[3] for elem in data]
            humidity_figure = figure(x_axis_type="datetime", plot_height = 300, y_range = (0,100))
            humidity_figure.line(times, humidity, legend_label = id + " humidity (%)", line_width=4)
            humidity_figure.xaxis.axis_label = "Time"
            humidity_figure.yaxis.axis_label = "Humidity (%)"

            script1, div1 = components(row(light_figure, humidity_figure))

            water = [elem[4] for elem in data]
            for i in range(len(water)):
                water[i] = (water[i]-1400)/2110 * 100
            water_figure = figure(x_axis_type="datetime", plot_height = 300, y_range = (0,100))
            water_figure.line(times, water, legend_label = id + " water (%)", line_width = 4, color = 'green')
            water_figure.xaxis.axis_label = "Time"
            water_figure.yaxis.axis_label = "Water (%)"

            temperature = [elem[5] for elem in data]
            temp_fig = figure(x_axis_type="datetime", plot_height = 300)
            temp_fig.line(times, temperature, legend_label = id + " temperature (degrees Fahrenheit)", line_width = 4, color='red')
            temp_fig.xaxis.axis_label = "Time"
            temp_fig.yaxis.axis_label = "Temperature (degrees Fahrenheit)"
            script2, div2 = components(row(temp_fig, water_figure))


            return f'''<!DOCTYPE html>
                <html> <script src="https://cdn.bokeh.org/bokeh/release/bokeh-2.3.0.min.js"></script>
                            <body>
                                {div1}
                    {div2}

                            </body>
                                {script1}
                    {script2}

                        </html>
                        '''
    else:
        return "Invalid request"