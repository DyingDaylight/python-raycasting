import logging
import array
import os


class PPMImage:
    
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        
        # array of bytes denoting color components
        self.framebuffer = array.array('B', [255, 255, 255] * self.width * self.height)
        
        # cache coordinates (x, y) -> x + y * width
        # TODO: check if it is faster
        self.cache = {}
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                self.cache[(x, y)] = 3 * int(x) + 3 * int(y) * self.width
        
        
    def get_bytes(self) -> bytearray:
        # get bytes for ppm foramt image
        # P6 - a "magic number" for identifying the file type
        # 255 - a maximum color value
        header = f"P6\n{self.width} {self.height}\n255\n"
        return bytearray(header, 'ascii') + bytes(self.framebuffer)
        
        
    def get_bytes_without_header(self) -> bytearray:
        # get bytes 
        print(len(self.framebuffer) % 3)
        return bytes(self.framebuffer)
        
    
    def flush(self) -> None:
        self.framebuffer = array.array('B', [255, 255, 255] * self.width * self.height)
    
    
    def draw_point(self, x: int, y: int, color: tuple) -> None:
        if len(color) != 3 or not all(0 <= comp <= 255 for comp in color):
            raise ValueError("Color should be three component tuple of ints 0-255")
            
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise ValueError(f"Invalid coordinates ({x}, {y})")
            
        index = self.cache[(x, y)]
        self.framebuffer[index:index + 3] = array.array('B', color)
        
        
    def draw_recatangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        if len(color) != 3 or not all(0 <= comp <= 255 for comp in color):
            raise ValueError("Color should be three component tuple of ints 0-255")
            
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise ValueError(f"Invalid coordinates ({x}, {y})")
            
        if x + width > self.width or y + height > self.height:
            raise ValueError(f"Invalid dimentions ({x} + {width}, {y} + {height}) out of {self.width} x {self.height}")
            
        for j in range(height):    
            start = self.cache[(x, y + j)]
            end = self.cache[(x + width, y + j)]
            self.framebuffer[start:end] =  array.array('B', list(color) * width)
    
    
    def write_to_file(self, filename: str = "output\output.ppm") -> None:
        """ Write image to .ppm file """        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if not filename.endswith(".ppm"):
            filename = filename + ".ppm"
        
        with open(filename, "wb") as image:
            image.write(self.get_bytes())
                
        logging.debug(f'Image is written to {filename}.')
        
        
