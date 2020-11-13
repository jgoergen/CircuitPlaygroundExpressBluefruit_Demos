import neopixel
import board
import struct
import math
import time
import sys
import analogio
import audiobusio
import array
import digitalio
import supervisor
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

NUM_PIXELS = 10
SENSOR_UPDATE_RATE_MS = 0.2
BLE_UPDATE_RATE_MS = 10

pixel = neopixel.NeoPixel(board.D8, NUM_PIXELS, pixel_order=neopixel.RGB)

light = analogio.AnalogIn(board.LIGHT)

mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16)

samples = array.array('H', [0] * 160)
mic.record(samples, len(samples))
lastSensorUpdate = 0
lastBLEUpdate = 0
runningSoundReadings = []
runningLightReadings = []


def mean(values):
    if (len(values) == 0):
        return 0

    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(sum_of_samples / len(values))


print("\033c")  # clear the terminal
print("Remote waiting for host...")
# Advertise when not connected.
ble.start_advertising(advertisement)

while not ble.connected:
    for i in range(NUM_PIXELS):
        pixel[i] = (50, 0, 0)

    pixel.show()
    time.sleep(1)

for i in range(NUM_PIXELS):
    pixel[i] = (0, 50, 0)

pixel.show()

# Connected
ble.stop_advertising()
print("CONNECTED")

while ble.connected:
    if uart_server.in_waiting:
        raw_bytes = uart_server.read(uart_server.in_waiting)
        text = raw_bytes.decode().strip()
        # print("raw bytes =", raw_bytes)
        print("RX:", text)

    if (time.monotonic() > (lastSensorUpdate + SENSOR_UPDATE_RATE_MS)):
        lastSensorUpdate = time.monotonic()

        runningLightReadings.append(light.value)
        print("Light " + str(light.value))

        try:
            mic.record(samples, len(samples))
            runningSoundReadings.append(normalized_rms(samples))
            print("Sound " + str(normalized_rms(samples)))
        except:
            pass

    if (time.monotonic() > (lastBLEUpdate + BLE_UPDATE_RATE_MS)):
        lastBLEUpdate = time.monotonic()

        print("Sending average sensor values...")
        uart_server.write(
            ("s|0|" + str(int(mean(runningSoundReadings)))).encode())
        uart_server.write(
            ("s|1|" + str(int(mean(runningLightReadings)))).encode())

        # reset running value arrays
        runningSoundReadings = []
        runningLightReadings = []

supervisor.reload()
