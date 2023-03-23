from Devices.temperatureprobe import TemperatureProbe
from Config.deviceconfigs import TemperatureConfig
from Repositories.iRepository import iRepository


class TemperatureRepository(iRepository):

    def __init__(self, probe=None):
        if probe is None:
            probe = TemperatureProbe(location=TemperatureConfig.location)

        self.probe = probe

    def get_temperature(self, matches):
        """route for /temperature"""
        temperaturehtmlfile = "Repositories/Temperature/Templates/temperature.html"
        htmlfile = open(temperaturehtmlfile, 'r')
        html = htmlfile.read()
        return str(html.format(temperature=self.probe.poll()))

    def get_routes(self):
        return {"GET": {"^\/temperature$": self.get_temperature}}
