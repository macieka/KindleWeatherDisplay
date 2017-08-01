#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012

import urllib2
from xml.dom import minidom
import datetime
import codecs
from pprint import pprint
from pyowm import OWM

api_key = '4c2f530274356fa51b07af049c960ed9'
city = 'Warsaw,PL'
owm = OWM(api_key)

obs = owm.weather_at_place(city)
# w = obs.get_weather()

fc = owm.daily_forecast(city)
f = fc.get_forecast()

highs = [None]*4
lows = [None]*4
icons = [None]*4

iconsMap = {'802': 'bkn', '801': 'bkn',
            601: 'sn', 602: 'blizzard', 611: 'sn', 612: 'sn',
            741: 'fg', 701: 'fg', 721: 'fg', 500: 'hi_shwrs', 501: 'hi_shwrs', 502: 'hi_shwrs', 503: 'hi_shwrs', 803: 'ovc', 804: 'ovc',
            300: 'ra', 301: 'ra', 302: 'ra', 310: 'ra', 311: 'ra', 312: 'ra', 313: 'ra', 314: 'ra', 321: 'ra',
            903: 'cold', 511: 'fzra', 904: 'hot', 210: 'scttsra', 201: 'scttsra', 202: 'scttsra', 211: 'scttsra', 212: 'scttsra', 221: 'scttsra',
            230: 'scttsra', 231: 'scttsra', 232: 'scttsra', 800: 'skc', 600: 'sn', 200: 'tsra', 905: 'wind', 957: 'wind',
            801: 'few', 616: 'mix', 621: 'mix', 622: 'mix', 615: 'rasn', 620: 'rasn', 802: 'ovc',
            }

lows[0] = int(obs.get_weather().get_temperature(unit='celsius')['temp_min'])
highs[0] = int(obs.get_weather().get_temperature(unit='celsius')['temp_max'])
icons[0] = iconsMap[obs.get_weather().get_weather_code()]

for i in range(1, 4):
    lows[i] = int(f.get_weathers()[i].get_temperature(unit='celsius')['min'])
    highs[i] = int(f.get_weathers()[i].get_temperature(unit='celsius')['max'])
    icons[i] = iconsMap[f.get_weathers()[i].get_weather_code()]

#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

now = datetime.datetime.now()
dtyear=str(now.year)
dtmonth=str(now.month)
dtday=str(now.day)
dthour=str(now.hour)
dtmin=str(now.minute)
dtnow=str(dtday+'/'+dtmonth+'/'+dtyear+' '+dthour+':'+dtmin)

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))
output = output.replace('DATE_VALPLACE',str(dtnow))

# Insert days of week
one_day = datetime.timedelta(days=1)
# date = datetime.datetime.fromtimestamp(obs.get_reception_time() / 1e3)
# xml_day_one = dom.getElementsByTagName('start-valid-time')[0].firstChild.nodeValue[0:10]
day_one = datetime.datetime.fromtimestamp(obs.get_reception_time())

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_ONE',days_of_week[(day_one + 0*one_day).weekday()]).replace('DAY_TWO',days_of_week[(day_one + 1*one_day).weekday()]).replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)
