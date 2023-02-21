import humidityprobe
import uasyncio
from Config.fileconfigs import humidityhtmlfile
from ConnectionProvider.connectionprovider import connect, open_socket
from humidityprobe import HumidityProbe
import re
import select


def get_request_method(request):
    """ return http request method """
    lines = request.split("\r\n")
    match = re.search("^(.+) /", lines[0])
    if match is None:
        return ""
    return match.group(1)


def get_request_query_string(request):
    """ return http request query string """
    lines = request.split("\r\n")
    match = re.search("^.+ (/.*) HTTP", lines[0])
    if match is None:
        return ""
    return match.group(1)


def gethtml(fileaddress):
    htmlfile = open(fileaddress, 'r')
    return htmlfile.read()


def webpage(fileaddress, humidity):
    htmlfile = open(fileaddress, 'r')
    html = htmlfile.read()
    return str(html.format(humidity=humidity))


def gethumidity():
    """route for /humidity"""
    htmlfile = open(humidityhtmlfile, 'r')
    html = htmlfile.read()
    return str(html.format(humidity=humidityprobe.HumidityProbe().poll()))


def getindex():
    """route for / and /index"""
    return gethtml("Templates/index.html")


def gettempreature():
    return gethtml("Templates/index.html")


def favicon():
    return open("favicon-32x32.png", 'rb').read()


def p():
    return ""


async def serve(conn):
    wrapped_conn = select.poll()
    wrapped_conn.register(conn, select.POLLIN)

    routes = {
        "GET": {
            "/": getindex,
            "/index": getindex,
            "/humidity": gethumidity,
            "/temperature": gettempreature,
            "/favicon.ico": favicon,
            "/favicon-32x32.png": favicon
        }
    }

    print(f"created poll object: {wrapped_conn}")
    while True:
        print("waiting for connection")
        try:
            events = wrapped_conn.poll(500)
            for sock, event in events:
                if event and select.POLLIN:
                    print(f"Connection! event: {event}")

                    client = conn.accept()[0]
                    request = client.recv(1024)
                    string_request = str(request.decode('UTF-8'))

                    # TO DO: Routing, but like better
                    method = get_request_method(string_request)
                    query = get_request_query_string(string_request)
                    bound_method = routes.get(method).get(query)

                    print(f"{method}: {query}: {bound_method.__name__}")

                    if bound_method is not None:
                        response = bound_method()
                        client.send(response)
                        print(f"sent {response}")

                    client.close()

            print(f"sleeping")
            await uasyncio.sleep(1)
        except Exception as e:
            print(f"Exception! {e}")


def createserver():
    ip = connect()
    sock = open_socket(ip)
    serve(sock)

