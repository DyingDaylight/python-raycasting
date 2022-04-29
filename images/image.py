import logging

from drawables import Drawable

# For PPMImage
import struct

# For PixmapImage
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

class Image:
    
    @staticmethod
    def get_image(width: int, height: int, is_gui: bool):
        if is_gui:
            return PixmapImage(width, height)
        else:
            return PPMImage(width, height)
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    
    def render(self, drawable: Drawable):
        pass
        
    def draw_point(self, x: int, y: int, r: int, g: int, b: int) -> None:
        pass
        
    def draw_recatangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        pass


class PPMImage(Image):
    
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.framebuffer = [self._pack_color(255, 255, 255)] * (self.width * self.height) # image initialized to white
        
        
    def render(self, drawable: Drawable):
        drawable.draw(self)

        
    def draw_point(self, x: int, y: int, r: int, g: int, b: int) -> None:
        self.framebuffer[int(x) + int(y) * self.width] = self._pack_color(r, g, b)


    def draw_recatangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        for i in range(width):
            for j in range(height):
                coord_x = x + i
                coord_y = y + j
                #if coord_x >= width or coord_y >= height:
                #    continue
                self.draw_point(coord_x, coord_y, *color)
    
    
    
    def flush(self):
        self.framebuffer = [self._pack_color(255, 255, 255)] * (self.width * self.height)
        
    def draw(self, x: int, y: int, color: tuple) -> None:
        self.draw_point(x, y, *color)        
        
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
        
        


class PixmapImage(Image):

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        
        self.pixmap = QPixmap(width, height)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.painter = QPainter()
        
        
    def render(self, drawable: Drawable):
        drawable.draw(self)
        
        
    def draw_point(self, x: int, y: int, r: int, g: int, b: int) -> None:
        self.painter.begin(self.pixmap)
        self.painter.setPen(QColor(r, g, b))
        self.painter.drawPoint(x, y)
        self.painter.end()
        
        
    def draw_recatangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        self.painter.begin(self.pixmap)
        self.painter.fillRect(x, y, width, height, QColor(*color))
        self.painter.end()