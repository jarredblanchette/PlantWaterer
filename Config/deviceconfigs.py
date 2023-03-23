from machine import Pin, ADC
from Devices.device import Device


class HumidityConfig(Device):
    location = ADC(Pin(28))

    min_value = 0
    max_value = 65535


class TemperatureConfig(Device):
    location = ADC(4)

    min_value = 0
    max_value = 65535

class I2CConfig(Device):
    sdaPin = Pin(0)
    sclPin = Pin(1)
    location = (sdaPin, sclPin)


class PumpConfig():
    location = Pin(16, Pin.OUT)



