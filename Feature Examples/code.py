import os
import adafruit_sdcard
import board
import busio
import digitalio
import storage

# from hackerbox 60: https://www.instructables.com/HackerBox-0060-Playground/

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


def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


print("Files on filesystem:")
print("====================")
print_directory("/sd")
