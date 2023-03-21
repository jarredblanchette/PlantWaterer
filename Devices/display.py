from Devices.ssd1306 import SSD1306_I2C
from Config.deviceconfigs import I2CConfig
from Devices.device import Device
from machine import I2C


class Display(SSD1306_I2C, Device):
    def __init__(self, location=None, width=None, height=None, i2c=None, line_height=None):
        if location is None:
            location = I2CConfig.location

        self.location = location

        if width is None:
            width = 128
        if height is None:
            height = 32
        if i2c is None:
            i2c = I2C(0, scl=self.location[1], sda=self.location[0])
        if line_height is None:
            line_height = 8

        self.width = width
        self.height = height
        self.i2c = i2c
        self.line_height = line_height

        super().__init__(self.width, self.height, self.i2c)

    def top_print(self, text):
        self.scroll(0, self.line_height)
        self.fill_rect(0, 0, self.width, self.line_height, 0)
        self.text(text, 0, 0)
        self.show()

    def bottom_print(self, text):
        self.scroll( 0, - self.line_height)
        self.fill_rect( 0, self.height - self.line_height, self.width, self.line_height, 0)
        self.text( text, 0, self.height - self.line_height)
        self.show()
