import network
import socket
import uasyncio
from ConnectionProvider import secrets
from machine import Pin


async def awaitEstablishedConnection(ssid, password, retry_seconds=0.2):
    led = Pin("LED", Pin.OUT)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        led.on()
        await uasyncio.sleep(retry_seconds / 2)
        led.off()
        await uasyncio.sleep(retry_seconds / 2)

    return wlan


async def connect(retry_seconds=0.2, max_wait_time_seconds=5):
    print(f"attempting to connect, initalising")

    print(f"wlan enabled")
    try:
        wlan = await uasyncio.wait_for(awaitEstablishedConnection(secrets.SSID, secrets.PASSWORD, retry_seconds)
                                       , max_wait_time_seconds)

        print(f"Success! Our IP is: {wlan.ifconfig()[0]}")
        return wlan.ifconfig()[0]
    #TODO: for some reason we're not able to find TimeoutError on the pico. Fix it.
    except TimeoutError as e:
        print(f"Failure, could not connect within timeout.  Error: {e}")
        return None
    except Exception as e:
        print(f"Failure, connection failed.  Error: {e}")
        return None


def open_socket(ip: str):
    print(f"initialising socket on: {ip}:80")
    address = (ip, 80)

    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    connection.bind(address)
    connection.listen(1)
    print(f"listening at ip: {ip}")

    return connection
