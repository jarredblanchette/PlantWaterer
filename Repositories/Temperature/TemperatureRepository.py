from Devices.temperatureprobe import TemperatureProbe
from Config.deviceconfigs import TemperatureConfig
from Repositories import iRepository


class TemperatureRepository(iRepository):

    def __int__(self, probe=None):
        if probe is None:
            probe = TemperatureProbe(location=TemperatureConfig.location)

        self.probe = probe

    def get_temperature(self):
        """route for /temperature"""
        humidityhtmlfile = "Templates/temperature.html"
        htmlfile = open(humidityhtmlfile, 'r')
        html = htmlfile.read()
        return str(html.format(temperature=self.probe.poll()))

    def get_routes(self):
        return {"GET": {"/temperature": self.get_temperature()}}
