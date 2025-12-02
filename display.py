from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
import time
import faces

class Display:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio_DC=27, gpio_RST=17, gpio_CS=22)
        self.device = sh1106(self.serial, width=128, height=64, rotate=2)

        self.device.clear()

        self.image = Image.new("1", (self.device.width, self.device.height))
        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype("fonts/DejaVuSansMono.ttf", 30)

        self.x, self.y = 2,0
        self.line_height = 32
        
        self.current_face = None
        self.frame = 1
        
        self.done = False

    def display_face(self):
        self.frame = 1
        
        while not self.done:
            frame_rate = self.current_face[0]
            self.draw.rectangle((0, 0, self.device.width, self.device.height), outline=0, fill=0)
            for line in self.current_face[self.frame]:
                self.draw.text((self.x,self.y), line, font=self.font, fill=255) 
                self.y += self.line_height
            self.y = 0
            if self.frame == len(self.current_face) - 1:
                self.frame = 1
            else:
                self.frame += 1
            self.device.display(self.image)
            time.sleep(1 / frame_rate)
        
    def clear(self):
        self.device.clear()

