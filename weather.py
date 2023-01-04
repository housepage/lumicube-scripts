import math
import requests
import datetime
from zoneinfo import ZoneInfo

leds = {}

display.set_all(black)

def safe_set(x, y, color):
    if x > -1 and x < 16 and y > -1 and y < 16:
        leds[(x,y)] = color

def draw_number(number, x_offset, y_offset):
    if number == 1:
        for y in range(0,5):
            safe_set(x_offset - 1, y_offset + y, white)
        safe_set(x_offset - 2, y_offset + 4, white)
        safe_set(x_offset - 2, y_offset, white)
        safe_set(x_offset, y_offset, white)
    elif number == 2:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset + 2, white)
            safe_set(x_offset - x, y_offset, white)
        safe_set(x_offset, y_offset + 3, white)
        safe_set(x_offset - 2, y_offset + 1, white)
    elif number == 3:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset, white)
        for y in range(1,4):
            safe_set(x_offset, y_offset + y, white)
        safe_set(x_offset - 1, y_offset + 2, white)
    elif number == 4:
        for y in range(0,5):
            safe_set(x_offset, y_offset + y, white)
        for y in range(2,5):
            safe_set(x_offset - 2, y_offset + y, white)
        safe_set(x_offset - 1, y_offset + 2, white)
    elif number == 5:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset + 2, white)
            safe_set(x_offset - x, y_offset, white)
        safe_set(x_offset, y_offset + 1, white)
        safe_set(x_offset - 2, y_offset + 3, white)
    elif number == 6:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset + 2, white)
            safe_set(x_offset - x, y_offset, white)
        safe_set(x_offset, y_offset + 1, white)
        safe_set(x_offset - 2, y_offset + 1, white)
        safe_set(x_offset - 2, y_offset + 3, white)
    elif number == 7:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
        for y in range(0,5):
            safe_set(x_offset, y_offset + y, white)
    elif number == 8:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset + 2, white)
            safe_set(x_offset - x, y_offset, white)
        safe_set(x_offset - 2, y_offset + 1, white)
        safe_set(x_offset, y_offset + 1, white)
        safe_set(x_offset - 2, y_offset + 3, white)
        safe_set(x_offset, y_offset + 3, white)
    elif number == 9:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset + 2, white)
        safe_set(x_offset - 2, y_offset + 3, white)
        safe_set(x_offset, y_offset + 3, white)
        for y in range(0,2):
            safe_set(x_offset, y_offset + y, white)
    elif number == 0:
        for x in range(0,3):
            safe_set(x_offset - x, y_offset + 4, white)
            safe_set(x_offset - x, y_offset, white)
        for y in range(0,5):
            safe_set(x_offset, y_offset + y, white)
            safe_set(x_offset - 2, y_offset + y, white)

def draw_two_digit_number(number, x_offset, y_offset):
    draw_number(math.trunc(number / 10), x_offset - 4, y_offset)
    draw_number(round(number % 10), x_offset, y_offset)

def current_weather():
    response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=47.527281&longitude=-122.372886&current_weather=true&temperature_unit=fahrenheit&timezone=PST')
    json_response = response.json()
    return json_response['current_weather']
    
def current_astronomy():
    response = requests.get('https://api.ipgeolocation.io/astronomy?apiKey=4f83e63f28aa4408b0bc5c6b4d0b3b25&lat=47.527281&long=-122.372886')
    json_response = response.json()
    return json_response
    
def current_time():
    zone = ZoneInfo("America/Los_Angeles")
    return datetime.datetime.now(zone).time()
    
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
    screen.write_text(0, 14, "Forecast: " + desc, 1, white, black)

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

def draw_weather(current_weather, current_astronomy):
    weather_code = current_weather['weathercode']
    print("Weather Code:", weather_code)
    weather_code = 0
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
            for i in range(0,15):
                leds[(random.randint(0,16), random.randint(0,16))] = yellow
            
    elif weather_code == 3:
        #Overcast
        forecast_to_screen("Overcast")
        for x in range(0,16):
            for y in range(0, 16):
                leds[(x,y)] = grey

while True:
    try:
        leds = {}
        current_weather = current_weather()
        print(current_weather)
        current_astronomy = current_astronomy()
        draw_weather(current_weather, current_astronomy)
        temperature = round(current_weather['temperature'])
        print("Temperature: ", temperature)
        draw_two_digit_number(temperature, 6, 0)
        display.set_all(black)
        display.set_leds(leds)
    except Exception as e:
        print("Error: ", e)
        pass
    time.sleep(300)


