import math
import requests

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

def draw_weather(current_weather):
    weather_code = current_weather['weathercode']
    print("Weather Code:", weather_code)
    if weather_code == 0:
        forecast_to_screen("Clear")
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
    elif weather_code == 3:
        #Overcast
        forecast_to_screen("Overcast")
        display.set_all(grey)

while True:
    try:
        display.set_all(black)
        leds = {}
        current_weather = current_weather()
        draw_weather(current_weather)
        draw_two_digit_number(current_weather['temperature'], 6, 0)
        display.set_leds(leds)
    except:
        pass
    time.sleep(300)


