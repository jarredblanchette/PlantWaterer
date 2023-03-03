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


class PumpConfig():
    location = Pin(0,Pin.OUT)



