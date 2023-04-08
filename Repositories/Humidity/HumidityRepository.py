from Devices.humidityprobe import HumidityProbe
from Repositories.iRepository import iRepository


class HumidityRepository(iRepository):

    def __init__(self, probe=None):
        if probe is None:
            probe = HumidityProbe()
        self.probe = probe

    def get_humidity(self):
        if self.probe is None:
            return
        return self.probe.poll()

    def get_humidity_html(self, matches=None):
        """route for /humidity"""
        if self.probe is None:
            return
        humidityhtmlfile = "Repositories/Humidity/Templates/humidity.html"
        htmlfile = open(humidityhtmlfile, 'r')
        html = htmlfile.read()
        return str(html.format(humidity=self.probe.poll()))

    def get_routes(self):
        return {"GET": {"^\/humidity$": self.get_humidity_html}}
