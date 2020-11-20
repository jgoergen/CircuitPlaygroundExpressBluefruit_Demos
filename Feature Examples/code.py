import os
import adafruit_sdcard
import board
import busio
import digitalio
import storage
import time
import neopixel
import adafruit_thermistor
import analogio
import simpleio
import audiobusio
import adafruit_lis3dh

# from hackerbox 60: https://www.instructables.com/HackerBox-0060-Playground/
# circuit playground express bluefruit info: https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/guided-tour

# bluetooth serial example here: https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/playground-bluetooth-plotter

try:
    from audiocore import WaveFile
except ImportError:
    from audioio import WaveFile

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# sd pin assignment from here: https://github.com/adafruit/circuitpython/issues/536
# sd example code here: https://learn.adafruit.com/adafruit-micro-sd-breakout-board-card-tutorial/circuitpython
# Use any pin that is not taken by SPI
SD_CS = board.A4

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.A3, board.A2, board.A1)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# accelerometer info here: https://circuitpython.readthedocs.io/projects/lis3dh/en/latest/examples.html
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Set tap detection to double taps.  The first parameter is a value:
#  - 0 = Disable tap detection.
#  - 1 = Detect single taps.
#  - 2 = Detect double taps.
# The second parameter is the threshold and a higher value means less sensitive
# tap detection.  Note the threshold should be set based on the range above:
#  - 2G = 40-80 threshold
#  - 4G = 20-40 threshold
#  - 8G = 10-20 threshold
#  - 16G = 5-10 threshold
lis3dh.set_tap(1, 120)

thermistor = adafruit_thermistor.Thermistor(
    board.TEMPERATURE, 10000, 10000, 25, 3950)

lightSensor = analogio.AnalogIn(board.LIGHT)

pixels = neopixel.NeoPixel(
    board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

onboardLED = digitalio.DigitalInOut(board.D13)
onboardLED.switch_to_output()

buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Enable the speaker
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True


def play_file_from_device_storage(filename):
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass


def play_file_from_sd(filename):
    wave_file = open("/sd/" + filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass


def writeTextToFileOnSD(filename, text):
    with open("/sd/" + filename, "a") as f:
        f.write(text)


def readTextFromFileOnSD(filename):
    with open("/sd/" + filename, "r") as f:
        line = f.readline()
        result = ""

        while line != '':
            result = result + f.readline()

        return result


def setAllLEDS(color):
    for i in range(10):
        pixels[i] = color
        pixels.show()


def getTempInFarenheight():
    return thermistor.temperature * 9 / 5 + 32


def getLightVal():
    return simpleio.map_range(lightSensor.value, 2000, 62000, 0, 9)


def getTilt():
    return [value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]


def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


x, y, z = getTilt()
print("Tilt: x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
print("Light " + str(getLightVal()))
print("Temperature " + str(getTempInFarenheight()))
print("Button A " + str(buttonA.value))
print("Button B " + str(buttonB.value))
print("Switch " + str(switch.value))

setAllLEDS((255, 255, 255))
time.sleep(1)
setAllLEDS((0, 0, 0))

TILT_UPDATE_WAIT = 10
lastTileUpdate = 0

while True:
    if buttonA.value:  # button is pushed
        onboardLED.value = True
    else:
        onboardLED.value = False

    if (time.monotonic() + TILT_UPDATE_WAIT > lastTileUpdate):
        lastTileUpdate = time.monotonic()

        if lis3dh.tapped:
            setAllLEDS((255, 255, 255))
            pixels.show()
            time.sleep(0.5)

        else:
            x, y, z = getTilt()
            fixedX = int(remap(x, -1, 1, 0, 10))
            fixedY = int(remap(y, -1, 1, 0, 10))
            fixedZ = int(remap(z, -1, 1, 0, 10))

            for i in range(10):
                r = 0
                g = 0
                b = 0

                if (fixedX == i):
                    r = 255

                if (fixedY == i):
                    g = 255

                if (fixedZ == i):
                    b = 255

                pixels[i] = (r, g, b)

            pixels.show()

    time.sleep(0.01)
