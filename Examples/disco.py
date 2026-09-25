import board
import busio
import digitalio
import random
import time
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis
from rainbowio import colorwheel


# some color definitions
OFF = (0, 0, 0)


# Create the I2C object for the trellis
i2c_bus = busio.I2C(board.SCL, board.SDA)
print(f"{i2c_bus.scan()=}")

# This is for a 2x2 array of NeoTrellis boards:
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2E, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x2F, auto_write=False)],
    [NeoTrellis(i2c_bus, False, addr=0x30, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x31, auto_write=False)],
]

trellis = MultiTrellis(trelli)

def intensity(xcoord, ycoord, edge):
    # Turn the LED on when a rising edge is detected
    if edge == NeoTrellis.EDGE_RISING:
        brightness = (8 - ycoord) / 8.0
        trellis.brightness = brightness
        print(f"{brightness=:.3f}  x={xcoord}, y={ycoord} pressed")

# Turn off all LEDs
for y in range(8):
    for x in range(8):
        trellis.color(x, y, OFF)
        # Activate rising edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.set_callback(x, y, intensity)

while True:
    try:
        trellis.sync()
        for y in range(8):
            for x in range(8):
                trellis.color(x, y, colorwheel(random.randrange(256)))
        trellis.show()
    except KeyboardInterrupt:
        # Turn off all LEDs
        print("\nLeaving the disco...")
        for y in range(8):
            for x in range(8):
                trellis.color(x, y, OFF)
        trellis.show()
        exit()
