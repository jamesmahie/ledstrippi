# LED Strip(show) using Raspberry Pi
# Code downloaded from https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html
# Original author: Tony DiCola (tony@tonydicola.com)
#

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 91      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
IE_LOGO_LEDS   = [2,36,37,72,74,             #(
                  4,33,40,76,                #i
                  6,                         #.
                  9,10,29,44,45,46,47,64,63, #e
                  13,                        #.
                  15,22,                     #,
                  17,19,54,55,89]            #)


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(1, strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=10, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(1, strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=10, iterations=2):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(1, strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(30):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def ieLogo(strip, wait_ms=500):
    """IE Logo interval flashes."""
    for j in range(1, strip.numPixels()):
        strip.setPixelColor(j, Color(0, 0, 0))
    for j in range(2):
        for i in IE_LOGO_LEDS:
            strip.setPixelColor(i, Color(255, 0, 0))
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(1, strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms/5000.0)
        for i in IE_LOGO_LEDS:
            strip.setPixelColor(i, Color(0, 255, 0))
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(1, strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms/5000.0)
        for i in IE_LOGO_LEDS:
            strip.setPixelColor(i, Color(0, 0, 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(1, strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms/5000.0)
        for i in IE_LOGO_LEDS:
            strip.setPixelColor(i, Color(255, 255, 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(1, strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms/5000.0)
        

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print ('Display IE logo.')
            ieLogo(strip)
            print ('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0), 20)  # Red wipe
            colorWipe(strip, Color(0, 255, 0), 20)  # Blue wipe
            colorWipe(strip, Color(0, 0, 255), 20)  # Green wipe
            print ('Display IE logo.')
            ieLogo(strip)
            print ('Theater chase animations.')
            theaterChase(strip, Color(127, 127, 127))  # White theater chase
            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            print ('Display IE logo.')
            ieLogo(strip)
            print ('Rainbow animation.')
            rainbow(strip)
            print ('Display IE logo.')
            ieLogo(strip)
            print ('Rainbow cycle animation.')
            rainbowCycle(strip, 5)
            print ('Display IE logo.')
            ieLogo(strip)
            print ('Rainbow chase animation.')
            theaterChaseRainbow(strip)
            print ('Display IE logo.')
            ieLogo(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)