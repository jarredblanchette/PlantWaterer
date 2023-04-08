import utime
from machine import Pin, I2C
from WebServer.web_server import WebServer
from ConnectionProvider.connnectionprovider import connect, open_socket
import uasyncio
from Repositories.Temperature.TemperatureRepository import TemperatureRepository
from Repositories.Humidity.HumidityRepository import HumidityRepository
from logger import Logger, Level
from Devices.display import Display
from water_plant import Waterer


async def periodically_update():
    while True:
        global mytime
        mytime = utime.time()
        # print(f"updating mytime to {mytime}")
        await uasyncio.sleep(10)


async def main(logger):
    led = Pin("LED", Pin.OUT)
    led.off()

    try:
        ip = await connect()
        print(f"my ip: {str(ip)}")
        connection = open_socket(ip)
        print(f"my socket: {connection}")
    except Exception as e:
        print(f"connection timed out, proceeding with no connection.  Error {e}")
        connection = None


    temp_repo = TemperatureRepository()
    humid_repo = HumidityRepository()
    repos = [temp_repo, humid_repo]

    plant_waterer = Waterer(period_seconds=5,logger=logger,poll_function=humid_repo.get_humidity)

    if connection is not None:
        server = WebServer()
        for repo in repos:
            server.add_routes(repo.get_routes())
        serverTask = uasyncio.create_task(server.serve(connection))

    watererTask = uasyncio.create_task(plant_waterer.run_waterer())
    # uasyncio.create_task(periodically_update())

    while True:
        logger.log(f'{utime.time()}', level=Level.Verbose)
        await uasyncio.sleep(1)


if __name__ == '__main__':
    logging_display = Display()
    logger = Logger(logging_display.bottom_print, Level.Error, True, True)
    uasyncio.run(main(logger))
