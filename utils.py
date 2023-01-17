from foundry_api.standard_library import *
import math

def LedDictionary():
    leds = {}
    for x in range(0,16):
        for y in range(0,16):
            if x < 8 or (x > 7 and y < 8):
                leds[x,y] = 0
    return leds

def safe_set(leds, x, y, color):
    if x > -1 and x < 16 and y > -1 and y < 16:
        leds[(x,y)] = color

def draw_number(leds, number, x_offset, y_offset):
    if number == 1:
        for y in range(0,5):
            safe_set(leds, x_offset - 1, y_offset + y, white)
        safe_set(leds, x_offset - 2, y_offset + 4, white)
        safe_set(leds, x_offset - 2, y_offset, white)
        safe_set(leds, x_offset, y_offset, white)
    elif number == 2:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset + 2, white)
            safe_set(leds, x_offset - x, y_offset, white)
        safe_set(leds, x_offset, y_offset + 3, white)
        safe_set(leds, x_offset - 2, y_offset + 1, white)
    elif number == 3:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset, white)
        for y in range(1,4):
            safe_set(leds, x_offset, y_offset + y, white)
        safe_set(leds, x_offset - 1, y_offset + 2, white)
    elif number == 4:
        for y in range(0,5):
            safe_set(leds, x_offset, y_offset + y, white)
        for y in range(2,5):
            safe_set(leds, x_offset - 2, y_offset + y, white)
        safe_set(leds, x_offset - 1, y_offset + 2, white)
    elif number == 5:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset + 2, white)
            safe_set(leds, x_offset - x, y_offset, white)
        safe_set(leds, x_offset, y_offset + 1, white)
        safe_set(leds, x_offset - 2, y_offset + 3, white)
    elif number == 6:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset + 2, white)
            safe_set(leds, x_offset - x, y_offset, white)
        safe_set(leds, x_offset, y_offset + 1, white)
        safe_set(leds, x_offset - 2, y_offset + 1, white)
        safe_set(leds, x_offset - 2, y_offset + 3, white)
    elif number == 7:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
        for y in range(0,5):
            safe_set(leds, x_offset, y_offset + y, white)
    elif number == 8:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset + 2, white)
            safe_set(leds, x_offset - x, y_offset, white)
        safe_set(leds, x_offset - 2, y_offset + 1, white)
        safe_set(leds, x_offset, y_offset + 1, white)
        safe_set(leds, x_offset - 2, y_offset + 3, white)
        safe_set(leds, x_offset, y_offset + 3, white)
    elif number == 9:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset + 2, white)
        safe_set(leds, x_offset - 2, y_offset + 3, white)
        safe_set(leds, x_offset, y_offset + 3, white)
        for y in range(0,2):
            safe_set(leds, x_offset, y_offset + y, white)
    elif number == 0:
        for x in range(0,3):
            safe_set(leds, x_offset - x, y_offset + 4, white)
            safe_set(leds, x_offset - x, y_offset, white)
        for y in range(0,5):
            safe_set(leds, x_offset, y_offset + y, white)
            safe_set(leds, x_offset - 2, y_offset + y, white)

def draw_two_digit_number(leds, number, x_offset, y_offset):
    draw_number(leds, math.trunc(number / 10), x_offset - 4, y_offset)
    draw_number(leds, round(number % 10), x_offset, y_offset)

def current_time():
    zone = ZoneInfo("America/Los_Angeles")
    return datetime.datetime.now(zone).time()
