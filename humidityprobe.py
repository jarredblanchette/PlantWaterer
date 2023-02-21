import uasyncio
from Config.deviceconfigs import HumidityConfig
from device import Device


class HumidityProbe(Device):
    def __init__(self, location=HumidityConfig.location, min_value=HumidityConfig.min_value,
                 max_value=HumidityConfig.max_value):
        self.min_value = min_value
        self.max_value = max_value
        self.location = location

    def poll(self):
        return (self.max_value - self.location.read_u16()) * 100 / (
                    self.max_value - self.min_value)
