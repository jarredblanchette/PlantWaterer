import network
import socket
import uasyncio
from ConnectionProvider import secrets
from machine import Pin


async def connect():
    print(f"attempting to connect, initalising")
    led = Pin("LED", Pin.OUT)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)

    print(f"wlan enabled")
    while not wlan.isconnected():
        print(f"Attempting to connect to {secrets.SSID}")
        led.on()
        await uasyncio.sleep(0.1)
        led.off()
        await uasyncio.sleep(0.1)

    led.off()
    print(f"Success! Our IP is: {wlan.ifconfig()[0]}")
    return wlan.ifconfig()[0]


def open_socket(ip: str):
    print(f"initialising socket on: {ip}:80")
    address = (ip, 80)

    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    connection.bind(address)
    connection.listen(1)
    print(f"listening at ip: {ip}")

    return connection
