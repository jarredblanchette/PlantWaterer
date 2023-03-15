import uasyncio
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


class WebServer:

    def __init__(self):
        self.routes = {
            "GET": {
                "/": self.getindex,
                "/favicon.ico": self.favicon,
                "/favicon-32x32.png": self.favicon,
            }
        }
        self.errors = {404: self.notfound}

    def get_routes(self):
        return self.routes

    def set_routes(self, routes):
        self.routes = routes

    def add_routes(self, new_routes):
        for method in new_routes:
            if method not in self.routes:
                self.routes[method] = {}
            for route in new_routes[method]:
                self.routes[method][route] = new_routes[method][route]

    # @staticmethod
    def getindex(self):
        """route for / and /index"""
        return gethtml("Templates/index.html").format(log=self.routes)

    @staticmethod
    def notfound():
        return gethtml("Templates/404.html")

    @staticmethod
    def favicon():
        return open("favicon-32x32.png", 'rb').read()

    async def serve(self, conn):
        wrapped_conn = select.poll()
        wrapped_conn.register(conn, select.POLLIN)

        while True:
            print(f"waiting for connection")
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
                        bound_method = self.routes.get(method).get(query)

                        if bound_method is None:
                            client.send(self.errors[404]())
                        else:
                            response = bound_method()
                            client.send(response)
                            print(f"sent {response}")

                        client.close()

                print(f"sleeping")
                await uasyncio.sleep(1)
            except Exception as e:
                print(f"Exception! {e}")
