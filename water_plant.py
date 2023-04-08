import uasyncio
import utime
from Config.deviceconfigs import PumpConfig
from logger import Level

class Waterer:

    def __init__(self, pump=None, water_for_seconds=None, min_humidity=None, poll_function=None, period_seconds=None, logger=None):
        """
        :param pump:
        :param water_for_seconds:
        :param min_humidity:
        :param poll_function:
        :param period_seconds:
        :param logger:
        """

        #TODO: refactor the way we're handling defaults, probably convert config to a json object.
        #not sure, because the idea of using objects with default values is neat
        if pump is None:
            pump = PumpConfig.location

        if water_for_seconds is None:
            water_for_seconds = 10

        if min_humidity is None:
            min_humidity = 30

        if poll_function is None:
            poll_function = lambda: None

        if period_seconds is None:
            period_seconds = 40

        if logger is None:
            logger = print

        self.pump = pump
        self.water_for_seconds = water_for_seconds
        self.min_humidity = min_humidity
        self.poll_function = poll_function
        self.period_seconds = period_seconds
        self.logger = logger

    async def run_pump(self, period=None, pump=None):
        if period is None:
            period = self.period

        if pump is None:
            pump = self.pump

        pump.on()
        await uasyncio.sleep(period)
        pump.off()

    async def run_waterer(self, water_for_seconds=None, poll_function=None):
        if poll_function is None:
            poll_function = self.poll_function

        if water_for_seconds is None:
            water_for_seconds = self.water_for_seconds

        while True:
            humidity = poll_function()
            self.logger.log(f"testing for watering at {utime.time()}",level=Level.Info)

            if humidity < self.min_humidity:
                self.logger.log(f"watering plant", level=Level.Info)
                await self.run_pump(water_for_seconds, self.pump)

            await uasyncio.sleep(self.period_seconds)
