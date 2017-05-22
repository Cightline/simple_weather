
import requests
import os
import json
import re

from pushbullet import Pushbullet

home          = os.getenv('HOME')
config_path   = '%s/.config/simple_weather/config.json' % (home)

with open(config_path, 'r') as cfg:
    config = json.load(cfg)

api_key         = config['api_key']
state           = config['state']
city            = config['city']
weather_dir     = '%s/.weather_watcher' % (home)
values_to_write = config['values_to_write']
#values_to_write = ['weather','temp_f', "precip_today_in"]
# color for polybar
polybar         = True

alert_url       = 'http://api.wunderground.com/api/%s/alerts/q/%s/%s.json' % (api_key, state, city)
condition_url   = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (api_key, state, city)



def get_page(url):
    
    page = requests.get(url)

    if page.status_code != 200:
        print('incorrect status code: %s' % (page.status_code))


    return page.json()


def write_to_file(name, data, lower=True):
    with open('%s/.simple_weather/%s' % (home,name), 'w') as f:

        if lower:
            f.write(str(data).lower())

        else:
            f.write(str(data))



condition_data = get_page(condition_url)['current_observation']

print(' '.join(condition_data.keys()))

for value in values_to_write:
    write_to_file(value, condition_data[value])


a = get_page(alert_url)['alerts']

if not a:
    print('No alerts')
    exit()


else:
    alert_data = []
    data = (get_page(alert_url)['alerts'])
    
    for alert in data:
        alert_data.append(alert)


    write_to_file(name, '/'.join(alert_data))
                



