#!/usr/bin/env python3
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import sys
import time
import board
import threading

ble = Adafruit_BluefruitLE.get_provider()


def startFirstBLEAdapter():
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()
    return adapter


def searchForDevice(adapter):
    print('Searching for UART device...', end="")
    device = None
    try:
        while (device is None):
            print(".", end='')
            adapter.start_scan()
            device = UART.find_device()
        print("OK")
    finally:
        adapter.stop_scan()

    device.connect()
    return device


def searchForUARTService(device):
    print('Discovering services...')
    UART.discover(device)
    uart = UART(device)
    return uart


def processBTMessage(message):
    messageSegments = message.split("|")
    if (messageSegments[0] == "s"):
        if (messageSegments[1] == "0"):
            print("Remote-Sound: " + messageSegments[2])
        elif (messageSegments[1] == "1"):
            print("Remote-Light: " + messageSegments[2])


def watchForBLEData(uart):
    received = None
    print("Watching for remote sensor data")

    while(True):
        received = uart.read()

        if received is not None:
            processBTMessage(received)
            received = None


def connectedLoop(uart):
    th = threading.Thread(target=watchForBLEData, args=(uart))
    th.start()

    while (True):
        print("Connected loop running...")
        time.sleep(1)


def main():
    print("\033c")  # clear the terminal
    # connect to bluetooth
    adapter = startFirstBLEAdapter()
    device = searchForDevice(adapter)

    try:
        uart = searchForUARTService(device)
        uart.write(b'c|reset|\r\n')
        print("Sent reset.")
        print("Starting message consume loop.")
        # wait for data, when received deal with it. forever and ever...
        connectedLoop(uart)

    finally:
        device.disconnect()


ble.initialize()
ble.run_mainloop_with(main)
