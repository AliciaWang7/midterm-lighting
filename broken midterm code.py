# import modules
import board
import time
import rotaryio
import time
import neopixel
from digitalio import DigitalInOut, Direction, Pull

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False, brightness=0.05)
knob = rotaryio.IncrementalEncoder(board.A1, board.A2)

# pixel colors
CLEAR = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (184, 38, 174)
pixels.value = False

# declare button objects
button = DigitalInOut(board.A3)
button.direction = Direction.INPUT
button.pull = Pull.UP
count_down = False
buttonPre = False

# define a function to scale and translate input value to output range

def scaleAndTranslate(inVal, inStart, inEnd, outStart, outEnd):
    # calculate incoming range
    inRange = inEnd - inStart
    # calculate a scale factor (percent) from the inVal in the inRange
    inProportion = (inVal - inStart) / inRange
    # calculate the output range
    outRange = outEnd - outStart
    # return the new value scaled and translated to the outRange
    return (inProportion * outRange) + outStart

time_keeper = 0
color = CLEAR
second_color = BLUE
pre_time = 1

while True:

    if button.value != buttonPre:
        buttonPre = button.value
        if not button.value:
            print("timer start")
            count_down = True
            start_time = time.monotonic()
            end_time = start_time + ((cur_pix * 10) + 10)

    if not count_down:
        # gather and scale input
        if knob.position < 0:
            knob.position = 0
        if knob.position > 72:
            knob.position = 72

        cur_pos = knob.position
        cur_time = int(scaleAndTranslate(cur_pos, 0, 24, 0, 9))
        cur_pix = cur_time

        time_keeper = cur_pix + 1
        print(cur_time, cur_pos, cur_pix)

        pixels.fill(color)
        pixels[cur_pix] = second_color
    else:
        # run the timer
        if time.monotonic() >= end_time:
            pixels.fill(RED)
        else:
            el_time = end_time - time.monotonic()
            pixels.brightness = scaleAndTranslate(el_time, 0, 100, 0, 1)
            pixels.fill(BLUE)

    pixels.show()

    time.sleep(0.01)