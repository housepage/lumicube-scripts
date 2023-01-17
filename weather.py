import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","AbstractFoundry","Daemon","Scripts")))

from utils import *

import threading
import math
import requests
import datetime
from zoneinfo import ZoneInfo
import traceback
import digitalrain

leds = LedDictionary()

display.set_all(black)

cached_weather = None

def current_weather():
    response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=47.527281&longitude=-122.372886&current_weather=true&temperature_unit=fahrenheit&timezone=PST')
    json_response = response.json()
    if "current_weather" in json_response:
        cached_weather = json_response["current_weather"]
        return cached_weather
    else:
        return cached_weather
    
def current_astronomy():
    response = requests.get('https://api.ipgeolocation.io/astronomy?apiKey=4f83e63f28aa4408b0bc5c6b4d0b3b25&lat=47.527281&long=-122.372886')
    json_response = response.json()
    return json_response
    
def moon_up(astronomy):
    now = current_time()
    moonrise = datetime.time.fromisoformat(astronomy["moonrise"])
    moonset = datetime.time.fromisoformat(astronomy["moonset"])
    
    return moonrise < now and now < moonset
    
def sun_up(astronomy):
    now = current_time()
    sunrise = datetime.time.fromisoformat(astronomy["sunrise"])
    sunset = datetime.time.fromisoformat(astronomy["sunset"])
    
    return sunrise < now and now < sunset

def forecast_to_screen(desc):
    screen.write_text(0, 16, "Forecast: " + desc, 1, white, black)
    
from enum import Enum

# class syntax

class Intensity(Enum):
    LIGHT = 1
    
def rain(intensity = Intensity.LIGHT):
    num_drops = intensity * 10
    drops = []


'''
WMO Weather interpretation codes (WW)
Code 	Description
0 	Clear sky
1, 2, 3 	Mainly clear, partly cloudy, and overcast
45, 48 	Fog and depositing rime fog
51, 53, 55 	Drizzle: Light, moderate, and dense intensity
56, 57 	Freezing Drizzle: Light and dense intensity
61, 63, 65 	Rain: Slight, moderate and heavy intensity
66, 67 	Freezing Rain: Light and heavy intensity
71, 73, 75 	Snow fall: Slight, moderate, and heavy intensity
77 	Snow grains
80, 81, 82 	Rain showers: Slight, moderate, and violent
85, 86 	Snow showers slight and heavy
95 * 	Thunderstorm: Slight or moderate
96, 99 * 	Thunderstorm with slight and heavy hail
'''

def rain(name):
    digitalrain.digitalrain(leds, 300, 1)

def draw_weather(current_weather, current_astronomy):
    weather_code = current_weather['weathercode']
    print("Weather Code:", weather_code)
    if weather_code == 0:
        forecast_to_screen("Clear")
        if sun_up(current_astronomy):
            for x in range(13, 16):
                for y in range(5, 8):
                    leds[(x,y)] = yellow
            for x in range(14, 16):
                leds[(x,4)] = orange
            for y in range(6, 8):
                leds[(12, y)] = orange
            leds[(13,5)] = orange
            for offset in range(1,3):
                leds[(13 - offset, 5 - offset)] = orange
                leds[(12 - offset, 6)] = orange
                leds[(15, 4 - offset)] = orange
        elif moon_up(current_astronomy):
            for x in range(14,16):
                for y in range(6,8):
                    leds[(x,y)] = white
                    leds[(y,x)] = white
        else:
           leds[(14,1)] = yellow
           leds[(15,4)] = yellow
           leds[(10,4)] = yellow
           leds[(11,1)] = yellow
           leds[(8,6)] = yellow
           leds[(6,7)] = yellow
           leds[(3,7)] = yellow
           leds[(0,7)] = yellow
           for star in range(0,4):
               leds[(random.randint(0,7), random.randint(8,15))] = yellow
    elif weather_code == 1:
        forecast_to_screen("Mainly Clear")
        for x in range(2,4):
            leds[(x,7)] = grey
            leds[(x + 4, 5)] = grey
            leds[(x + 9, 6)] = grey
            leds[(x + 6, 3)] = grey
    elif weather_code == 2:
        forecast_to_screen("Partly Cloudly")
        for x in range(2,5):
            leds[(x - 2, 7)] = grey
            leds[(x - 2, 6)] = grey
            leds[(x + 3, 5)] = grey
            leds[(x + 3, 4)] = grey
            leds[(x + 9, 6)] = grey
            leds[(x + 9, 5)] = grey
            leds[(x + 7, 2)] = grey
            leds[(x + 7, 1)] = grey
            
    elif weather_code == 3:
        #Overcast
        forecast_to_screen("Overcast")
        for x in range(0,16):
            for y in range(0, 16):
                leds[(x,y)] = grey
    elif weather_code == 51:
        print("Before starting the rain")
        # Rain
        # https://github.com/RaspiColas/lumicube/blob/main/digitalrain.py
        #x = threading.Thread(target=rain, args=(1,))
        #x.start()
        print("After starting the rain")
        
    elif weather_code == None:
        pass

def clear_screen():
    screen.draw_rectangle(0, 0, 319, 239, black)
    
    

while True:
    try:
        clear_screen()
        screen.write_text(0,0, "Viz: Weather", 1, white, black)
        leds = {}
        weather = current_weather()
        astronomy = current_astronomy()
        draw_weather(weather, astronomy)
        temperature = round(weather['temperature'])
        
        draw_two_digit_number(leds, temperature, 6, 0)
        display.set_leds(leds)
    except Exception as e:
        print("Error: ", e)
        traceback.print_exception(*sys.exc_info())
        pass
    time.sleep(300)


