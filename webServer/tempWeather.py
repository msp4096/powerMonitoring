#!/usr/bin/python

import urllib.request as urllib2, json

print('weather...')
#api_conditions_url = "http://api.wunderground.com/api/" + WUNDERGROUND_API_KEY + "/conditions/q/" + STATE + "/" + CITY + ".json"
api_conditions_url = "http://api.openweathermap.org/data/2.5/weather?id=4930505&appid=6ab5a0a32767ee7008260b57269d8c34"
try:
    with urllib2.urlopen(api_conditions_url) as url:
        f = json.loads(url.read().decode())
        #print(f)
#print(f)

except:
    print("Failed to get conditions")
    #return False
outside_conditions = f
temp_k = outside_conditions['main']['temp']
wind_speed = outside_conditions['wind']['speed']
temp_F = round((temp_k-273.0) * 9.0 /5.0 +32.0, 2)
print(temp_F)
print(wind_speed)
#json_conditions = f.read()
#f.close()
#print(json.loads(json_conditions))
