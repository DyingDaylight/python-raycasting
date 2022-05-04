import logging
import struct
import array

from drawables import Drawable


class PPMImage:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
         
        self.framebuffer = array.array('B', [255, 255, 0] * self.width * self.height)
        self.cache = {}
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                self.cache[(x, y)] = 3 * int(x) + 3 * int(y) * self.width
        
        
    def get_bytes(self):
        # P6 - a "magic number" for identifying the file type
        # 255 - a maximum color value
        header = f"P6\n{self.width} {self.height}\n255\n"
        return bytearray(header, 'ascii') + bytes(self.framebuffer)
    
    
    def draw_point(self, x: int, y: int, r: int, g: int, b: int) -> None:
        index = self.cache[(x, y)]
        self.framebuffer[index:index + 3] =  array.array('B', [r, g, b])
        
        
    def draw_recatangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        for j in range(height):    
            start = self.cache[(x, y + j)]
            end = self.cache[(x + width, y + j)]
            self.framebuffer[start:end] =  array.array('B', list(color) * width)
    

    
    
    def flush(self):
        #self.framebuffer = [self._pack_color(255, 255, 255)] * (self.width * self.height)
        self.framebuffer = array.array('B', [255, 255, 255] * self.width * self.height)
               
        
    def drop(self, filename: str) -> None:
        """ Drop image to .ppm file """        
        if not filename.endswith(".ppm"):
            filename = filename + ".ppm"
        
        with open(filename, "wb") as image:
            image.write(self.get_bytes())
                
        logging.debug(f'{filename} is dropped')
        
        
