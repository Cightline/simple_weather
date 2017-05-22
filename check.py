
import requests
import os
import os.path
import json
import re

from pushbullet import Pushbullet

home          = os.getenv('HOME')
write_dir     = '%s/.simple_weather' % (home)
config_path   = '%s/.config/simple_weather/config.json' % (home)

with open(config_path, 'r') as cfg:
    config = json.load(cfg)



if not os.path.exists(write_dir):
    os.makedirs(write_dir)
    print('created %s' % (write_dir))


api_key         = config['api_key']
state           = config['state']
city            = config['city']
weather_dir     = '%s/.weather_watcher' % (home)
values_to_write = config['values_to_write']
#values_to_write = ['weather','temp_f', "precip_today_in"]
# color for polybar
polybar         = config['polybar']
i3              = config['i3']

alert_url       = 'http://api.wunderground.com/api/%s/alerts/q/%s/%s.json' % (api_key, state, city)
condition_url   = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (api_key, state, city)



def get_page(url):
    
    page = requests.get(url)

    if page.status_code != 200:
        print('incorrect status code: %s' % (page.status_code))


    return page.json()


def write_to_file(name, data, lower=True):
    with open('%s/%s' % (write_dir, name), 'w') as f:

        if lower:
            f.write(str(data).lower())

        else:
            f.write(str(data))



condition_data = get_page(condition_url)['current_observation']

# Print the keys 
#print(' '.join(condition_data.keys()))

for value in values_to_write:
    write_to_file(value, condition_data[value])


a = get_page(alert_url)['alerts']

if not a:
    write_to_file('alerts', 'none')


else:
    alert_data = []
    data = (get_page(alert_url)['alerts'])
    
    for alert in data:
        alert_data.append(alert)


    if polybar:
        write_to_file('alerts', "%%{F#f00} %s" % ('/'.join(alert_data)))

    elif i3:
        write_to_file('alerts', "<span color='red'>%s</span>" % ('/'.join(alert_data)))

                



