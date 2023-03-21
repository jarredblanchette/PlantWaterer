class Level:
    Verbose = 9
    Debug = 7
    Error = 5
    Warn = 3
    Info = 0
    Disabled = -99

    @staticmethod
    def int_to_string(i):
        values = {9: "Verbose",
                  7: "Debug",
                  5: "Error",
                  3: "Warn",
                  0: "Info",
                  -99: "Disabled"
                  }

        if i in values:
            return values[i]

        return None


class Logger(object):
    def __init__(self, destination, level, include_level,minimal_header):
        if level is None:
            level = Level.Error
        self.level = level

        if destination is None:
            destination = print
        self.destination = destination

        if include_level is None:
            include_level = True
        self.include_level = include_level

        if minimal_header is None:
            minimal_header = False
        self.minimal_header = minimal_header

    def log(self, message, level):
        if level < self.level or self.level == Level.Disabled:
            return

        if self.include_level:
            if self.minimal_header:
                header = Level.int_to_string(level)[0] + ": "
            else:
                header = Level.int_to_string(level)+': '.ljust(16)
            message = f"{header}{message}"

        self.destination(message)
