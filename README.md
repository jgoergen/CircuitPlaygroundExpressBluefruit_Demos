# Adafruit Circuit Playground Express Bluefruit Demos
A collection of simple python scripts for the Adafruit Circuit Playground Express Bluefruit microcontroller board.

These can be purchased from [Here](https://www.adafruit.com/product/4333).

## Initial Setup of device:
### information taken from the [Adafruit Guide](https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython)
1) Note the version number and download the latest stable .uf2 CircuitPython file from [here](https://circuitpython.org/board/circuitplayground_bluefruit/).
2) Double click the reset button on the device and it will restart and have all leds solid red.
3) Plug the device into the computer if it isn't already, you should see a new drive appear named "CPLAYBTBOOT".
4) Open "CPLAYBTBOOT" drive, copy the previously downloaded uf2 file onto it and allow it to restart automatically.
5) Once it's done restarting you should have a different drive appear named "CIRCUITPY".
6) Download the latest library bundle for your previously downloaded version of CircuitPython from [Here}(https://circuitpython.org/libraries).
7) Becuase the size of the libraries will exceed the size of your "CIRCUITPY" drive by themselve at this point, you will want to hand copy what you need into the "CIRCUITPY/lib/" directory on your devices drive. I tend to just copy most of them, omitting stuff for devices I know I won't use. This saves me time later as I code.

## Debugging from your computer
* Download Putty from [Here](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
*   This app is useful for connecting to your device for debugging. When your device is connected and running code (your drive name will be named "CIRCUITPY".)
*   If you look at the COM ports on your computer you'll see the device has one open, connect to it at 9600 baud via Putty to see script errors, print statements, etc.
*   You can also press Control + C to stop a running script and control + D to restart it.

## Developing python on your computer
* I love vscode for developing python, personally. You'll also find alot of good plugins for 'linting' your python script and autoformatting it which saves alot of time.
