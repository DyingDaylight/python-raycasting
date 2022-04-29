import logging
import struct

from drawables import Drawable

class PPMImage:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.framebuffer = [self._pack_color(255, 255, 255)] * (self.width * self.height) # image initialized to red
        
        
    def flush(self):
        self.framebuffer = [self._pack_color(255, 255, 255)] * (self.width * self.height)
    
    
    def set_color(self, x: int, y: int, r: int, g: int, b: int) -> None:
        self.framebuffer[int(x) + int(y) * self.width] = self._pack_color(r, g, b)
        
        
    def render(self, drawable: Drawable):
        drawable.draw(self)
        
        
    def draw(self, x: int, y: int, color: tuple) -> None:
        self.set_color(x, y, *color)
    
    
    def draw_recatangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        for i in range(width):
            for j in range(height):
                coord_x = x + i
                coord_y = y + j
                #if coord_x >= width or coord_y >= height:
                #    continue
                self.set_color(coord_x, coord_y, *color)
        
        
    def drop(self, filename: str) -> None:
        """ Drop image to .ppm file """
    
        # P6 - a "magic number" for identifying the file type
        # 255 - a maximum color value
        header = f"P6\n{self.width} {self.height}\n255\n"
        
        if not filename.endswith(".ppm"):
            filename = filename + ".ppm"
        
        with open(filename, "wb") as image:
            image.write(bytearray(header, 'ascii'))
            
            for i in self.framebuffer:
                r, g, b, a = self._unpack_color(i)
                
                # Color components to byte objects packed to unsigned chars
                image.write(struct.pack('B', r)) 
                image.write(struct.pack('B', g))
                image.write(struct.pack('B', b))
                
        logging.debug(f'{filename} is dropped')
        
        
    def _pack_color(self, r: int, g: int, b: int, a: int=255) -> int:
        return (a << 24) + (b << 16) + (g << 8) + r
                
    def _unpack_color(self, color: int) -> (int, int, int, int):
        return color >> 0 & 255, color >> 8 & 255, color >> 16 & 255, color >> 24 & 255