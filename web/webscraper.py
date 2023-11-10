import requests
from bs4 import BeautifulSoup

def format_query(plant):
    query_string = ''
    split_name = plant.split()
    for word in split_name:
        query_string += word + '+'
    return query_string[0:-1]

def request_handler(request):
    if 'len' not in request['values'] or 'topic' not in request['values']:
        return 'Please enter a plant to look up'
    if request['values']['topic'] is None or request['values'] is None:
        return 'Please enter a plant to look up'
    formatted_plant = format_query(request['values']['topic'])
    to_send = 'https://pfaf.org/user/Plant.aspx?LatinName={}'.format(formatted_plant)
    r = requests.get(to_send)
    if r.text is None or r.text == "None":
        return 'Query did not go through. Make sure you are using correct name.'
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.get_text().split('Physical Characteristics')[1].split('UK Hardiness Map')[0].strip() == '' or soup.get_text().split('Physical Characteristics')[1].split('UK Hardiness Map')[0].strip() is None:
        return 'Query did not go through. Make sure you are using correct name.'
    return soup.get_text().split('Physical Characteristics')[1].split('UK Hardiness Map')[0] 

request = {'method': 'GET', 'values': {'topic': 'pee pee poo poo', 'len': 1}}
print(request_handler(request))
