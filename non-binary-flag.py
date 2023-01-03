# Draw a rainbow pattern.

leds = {}

display.set_all(black)

light_purple = hsv_colour(.84,.59,.93)

for x in range(8):
    for y, color in [(7, yellow),(6,yellow),(5,white),(4,white),(3,light_purple),(2,light_purple),(1,black),(0,black)]:
        for x_with_offset, y_with_offset in [(x,y),(x + 8, y),(7-y, x + 8)]:
            leds[x_with_offset, y_with_offset] = color

display.set_leds(leds)
