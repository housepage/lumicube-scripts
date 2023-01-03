import time
import random
import os
import threading

screen.write_text(0,0, "Viz: Cityscape", 1, white, black)

#x: 8-15
#y: 0-7

leds = {}

display.set_all(black)

for y in range(3,8):
    if y % 2 == 0:
        leds[(4,y)] = yellow
        leds[(6,y)] = yellow
        leds[(8,y)] = yellow
        leds[(10,y)] = yellow
    else:
        leds[(4,y)] = green
        leds[(6,y)] = green
        leds[(8,y)] = green
        leds[(10,y)] = green
    
    leds[(3,y)] = green
    leds[(5,y)] = green
    leds[(7,y)] = green    
    leds[(9,y)] = green
    leds[(11,y)] = green
    
for x in range(13,16):
    print(x)
    leds[(x,5)] = grey
    leds[(x,4)] = magenta
    leds[(x,3)] = magenta
    
for x in range(0,2):
    leds[(x,6)] = red
    leds[(x,5)] = cyan
    leds[(x,4)] = cyan
    leds[(x,3)] = cyan
    
for x in range(3,8):
    for y in range(8,12):
        leds[(x,y)] = green
   
# Moon
leds[(15,7)] = white
leds[(14,7)] = white
leds[(7,15)] = white
leds[(6,15)] = white
leds[(7,14)] = white
leds[(6,14)] = white

for x in range(0,16):
    leds[(x,2)] = purple

def safe_set(x, y, color):
    if x > -1 and x < 16 and y > -1 and y < 16:
        leds[(x,y)] = color

def draw_car(x_offset, y_offset, direction):
    for x in range(0,16):
        for y in range(y_offset,y_offset + 2):
            leds[(x,y)] = black
    safe_set(x_offset, y_offset, orange)
    safe_set(x_offset + 1, y_offset, orange)
    safe_set(x_offset + 2, y_offset, orange)
    safe_set(x_offset + 3, y_offset, orange)
    safe_set(x_offset + 1, 1 + y_offset, orange)
    safe_set(x_offset + 2, 1 + y_offset, orange)
    
    if direction == 'R':
        safe_set(x_offset + 4, y_offset, yellow)
        safe_set(x_offset + 5, y_offset, yellow)
    elif direction == 'L':
        safe_set(x_offset - 1, y_offset, yellow)
        safe_set(x_offset - 2, y_offset, yellow)


def play_random_soundscape(name):
    sound_dir = '/home/lumi/AbstractFoundry/Daemon/Sounds/'
    speaker.volume = 2
    while True:
        sound = random.choice(os.listdir(sound_dir))
        screen.write_text(0,16, "Sound: " + str(sound), 1, white, black)
        full_path = sound_dir + sound
        print(full_path)
        speaker.play(full_path)
        time.sleep(random.randrange(30,120))
        
x = threading.Thread(target=play_random_soundscape, args=(1,))
x.start()

while True:
    direction = random.choice(['L','R'])

    generated = None

    if direction == 'L':
        generated = range(19, -5, -1)
    elif direction == 'R':
        generated = range(0,19)

    for x_offset in generated:
        draw_car(x_offset,0, direction)
        display.set_leds(leds)
        time.sleep(0.25)

