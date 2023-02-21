from Config.deviceconfigs import TemperatureConfig
from device import Device


class TemperatureProbe(Device):
    def __init__(self, location=TemperatureConfig.location, min_value=TemperatureConfig.min_value,
                 max_value=TemperatureConfig.max_value):
        """:param: min_value is not used
        :param: max_value is not used"""
        self.min_value = min_value
        self.max_value = max_value
        self.location = location

    def poll(self):
        return 27 - (self.location.read_u16() - 0.706) / 0.001721
