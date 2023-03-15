from Devices.humidityprobe import HumidityProbe
from Config.deviceconfigs import HumidityConfig
from Repositories.iRepository import iRepository


class HumidityRepository(iRepository):

    def __init__(self, probe=None):
        if probe is None:
            probe = HumidityProbe(location=HumidityConfig.location,
                                  min_value=HumidityConfig.min_value,
                                  max_value=HumidityConfig.max_value)

        self.probe = probe

    def get_humidity(self):
        """route for /humidity"""
        humidityhtmlfile = "Repositories/Humidity/Templates/humidity.html"
        htmlfile = open(humidityhtmlfile, 'r')
        html = htmlfile.read()
        return str(html.format(humidity=self.probe.poll()))

    def get_routes(self):
        return {"GET": {"/humidity": self.get_humidity}}
