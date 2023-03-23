from Config.deviceconfigs import TemperatureConfig
from Devices.device import Device


class TemperatureProbe(Device):
    def __init__(self, location=None, min_value=None, max_value=None):
        """:param: min_value is not used
        :param: max_value is not used"""

        # use defaults if not provided
        if location is None:
            location = TemperatureConfig.location
        if min_value is None:
            min_value = TemperatureConfig.min_value
        if max_value is None:
            max_value = TemperatureConfig.max_value

        self.location = location
        self.min_value = min_value
        self.max_value = max_value

    def poll(self):
        return 27 - (self.location.read_u16() - 0.706) / 0.001721
