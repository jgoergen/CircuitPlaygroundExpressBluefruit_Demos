# Bluetooth serial connection between Circuit Playground Express Bluefruit and Raspberry pi.

This example connects to the raspberry pi and sends it averaged sound and light sensor data periodically.

## Setup notes
* The raspberry pi python script is written to be used with Python 3.
* You'll need to install a few libraries to use my example: ```sudo pip3 install RPI.GPIO adafruit-blinka```
* You'll need git installed to pull down the Adafruit Bluetooth library: ```sudo apt install git```
* Install linux specific bluetooth libs: ```sudo apt-get install bluetooth bluez blueman pi-bluetooth```
* Pull down Adafruit Bluetooth library: ```git clone https://github.com/adafruit/Adafruit_Python_BluefruitLE.git```
###Huge thanks to donatieng for patching gatt.py to make it work with newer versions of BlueZ!!! [info here](https://github.com/donatieng/Adafruit_Python_BluefruitLE/commit/af46b05cbcfd82110c8bbd08ed3d483de128fed1).
* Open the file gatt.py for editing ```sudo nano Adafruit_Python_BluefruitLE/master/Adafruit_BluefruitLE/bluez_dbus/gatt.py```
* Replace contents of function named ```__init__``` with
```
def __init__(self, dbus_obj):
        """Create an instance of the GATT service from the provided bluez
        DBus object.
        """
        self._obj = dbus_obj
        self._service = dbus.Interface(dbus_obj, _SERVICE_INTERFACE)
        self._props = dbus.Interface(dbus_obj, 'org.freedesktop.DBus.Properties')
```
* Replace contents of function named ```list_characteristics``` with
```
def list_characteristics(self):
        """Return list of GATT characteristics that have been discovered for this
        service.
        """
        return map(BluezGattCharacteristic, 
            get_provider()._get_objects(_CHARACTERISTIC_INTERFACE,
                                        self._service.object_path))
```
* Replace contents of function named ```read_value``` with
```
def read_value(self):
        """Read the value of this characteristic."""
        return self._characteristic.ReadValue({})
```
* Replace contents of function named ```write_value``` with
```
def write_value(self, value):
        """Write the specified value to this characteristic."""
        self._characteristic.WriteValue(value, {})
```
* Move into "Adafruit_python_bluefruitle" directory ```cd Adafruit_Python_BluefruitLE```
* Install ```sudo python3 setup.py install```