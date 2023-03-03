import uasyncio
from Config.deviceconfigs import HumidityConfig
from Devices.device import Device


class HumidityProbe(Device):
    def __init__(self, location=None, min_value=None, max_value=None):

        if location is None:
            location = HumidityConfig.location
        if min_value is None:
            min_value = HumidityConfig.min_value
        if max_value is None:
            max_value = HumidityConfig.max_value

        self.location = location
        self.min_value = min_value
        self.max_value = max_value

    def poll(self):
        return (self.max_value - self.location.read_u16()) * 100 / (
                    self.max_value - self.min_value)
