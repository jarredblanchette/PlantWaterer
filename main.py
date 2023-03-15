import utime
from machine import Pin
from WebServer.web_server import WebServer
from ConnectionProvider.connnectionprovider import connect,open_socket
import uasyncio
from Repositories.Temperature.TemperatureRepository import TemperatureRepository
from Repositories.Humidity.HumidityRepository import HumidityRepository

mytime = utime.time()


async def periodically_update():
    while True:
        global mytime
        mytime = utime.time()
        # print(f"updating mytime to {mytime}")
        await uasyncio.sleep(10)


async def main():
    led = Pin("LED", Pin.OUT)
    led.off()



    ip = await connect()
    print(f"my ip: {str(ip)}")
    connection = open_socket(ip)
    print(f"my socket: {connection}")

    temp_repo = TemperatureRepository()
    humid_repo = HumidityRepository()
    repos = [temp_repo, humid_repo]

    server = WebServer()
    for repo in repos:
        server.add_routes(repo.get_routes())

    serverTask = uasyncio.create_task(server.serve(connection))
    # watererTask = uasyncio.create_task(run_waterer(5, 40, sp, 10))
    # uasyncio.create_task(periodically_update())

    # print(f"hello from the main thread")
    # wrapped_my_time = select.poll()
    # wrapped_my_time.register(mytime)
    while True:
        # events = wrapped_my_time.poll(500)
        # for sock, event in events:
        #     if event and select.POLLIN:
        # print(f"mainthread: mytime is {mytime}")
        await uasyncio.sleep(1)


if __name__ == '__main__':
    # level = logging.INFO
    # logging.basicConfig(level=level)
    uasyncio.run(main())

