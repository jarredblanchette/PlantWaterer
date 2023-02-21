import uasyncio
from machine import Pin
from Config.deviceconfigs import PumpConfig


async def run_pump(s=1):
    print(f"turning pump on")
    pump = PumpConfig.location
    pump.on()
    await uasyncio.sleep(s)
    print(f"turning pump off")
    pump.off()


async def run_waterer(water_for, min_humidity, humidity_probe, period):
    while True:
        print(f"reading humiditiy")
        humidity = humidity_probe.poll()
        print(f"humiditiy is {humidity}")

        if humidity < min_humidity:
            await run_pump(water_for)

        await uasyncio.sleep(period)
