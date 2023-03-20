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

        #This is required, as micropython does not support quantifier capturing.
        #IE, r".{3}" will silently fail to match 3 chars
        #As such, the below mess is equilivent to:
        #uuid_regex = '[a-f\d]{8}\-(?:[a-f\d]{4}\-){3}[a-f\d]{12}'
        #TODO: make a function to do this programatically rather than manually converting
        uuid_regex = '[a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d]\-(?:[a-f\d][a-f\d][a-f\d][a-f\d]\-)(?:[a-f\d][a-f\d][a-f\d][a-f\d]\-)(?:[a-f\d][a-f\d][a-f\d][a-f\d]\-)[a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d][a-f\d]'

        self.routes = {
            "GET": {
                "^\/$": self.getindex,
                "^\/favicon\.ico$": self.favicon,
                "^\/favicon\-32x32\.png$": self.favicon,
                f"^\/example\/({uuid_regex})$": self.getexample
            }
        }
        self.errors = {404: self.notfound, 500: self.servererror}

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

    def get_restful_method(self, method, query):
        # return self.routes.get(method).get(query)
        print(f"routing the following: `{method}`.`{query}`")
        routes = self.routes.get(method)
        if routes is None:
            return None

        for route_regex in routes:
            matches = re.search(route_regex, query)
            print(f"trying: {route_regex}")
            if matches:
                print(f"routing to: {self.routes.get(method).get(route_regex)}")
                return matches, self.routes.get(method).get(route_regex)
            print(f"no match")
        return None


    def getexample(self, matches):
        return gethtml("Templates/index.html").format(log=f"group caught: {matches.group(1)}")

    # @staticmethod
    def getindex(self, matches):
        """route for / and /index"""
        return gethtml("Templates/index.html").format(log=self.routes)

    @staticmethod
    def notfound(matches):
        return gethtml("Templates/404.html")

    @staticmethod
    def servererror(matches):
        return gethtml("Templates/500.html")

    @staticmethod
    def favicon(matches):
        return open("favicon-32x32.png", 'rb').read()

    async def serve(self, conn):
        wrapped_conn = select.poll()
        wrapped_conn.register(conn, select.POLLIN)

        while True:
            # print(f"waiting for connection")
            try:
                events = wrapped_conn.poll(500)
                for sock, event in events:
                    if event and select.POLLIN:
                        print(f"Connection! event: {event}")

                        try:
                            client = conn.accept()[0]
                            request = client.recv(1024)
                            string_request = str(request.decode('UTF-8'))

                            # TO DO: Routing, but like better
                            method = get_request_method(string_request)
                            query = get_request_query_string(string_request)
                            matches, bound_method = self.get_restful_method(method, query)

                            if bound_method is None:
                                client.send(self.errors[404](None))
                            else:
                                response = bound_method(matches)
                                client.send(response)
                                print(f"sent {response}")

                        except Exception as e:
                            client.send(self.errors[500](None))
                            print(f"Exception! Tried to send 500. {e}")
                        finally:
                            client.close()

                # print(f"no connections, sleeping")
                await uasyncio.sleep(1)
            except Exception as e:
                print(f"Exception! {e}")
