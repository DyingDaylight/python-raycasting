import logging
import math
from random import randrange

from PIL import Image

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from images.image import Image

class Drawable:

    def __init__(self):
        pass
        
    def draw(self, output):
        logging.debug("draw(output) is not implemented")
        
        
class Player(Drawable):
    
    def __init__(self, x: int, y: int):
        # player's position
        self.x = x
        self.y = y
        
        # player's view direction
        self.a = math.pi
        self.a = 1.523
        self.fov = math.pi / 3
        
        # playes's size
        self.width = 5
        self.height = 5


    def draw(self, output):
        output.draw_recatangle(int(self.x * self.world.cell_width), 
                               int(self.y * self.world.cell_height), 
                               self.width, self.height, 
                               (160, 160, 160))
        
        
        end = int(math.sqrt(self.world.width ** 2 + self.world.height ** 2))
        
        for i in range(output.width // 2):
            angle = self.a - self.fov / 2 + self.fov * i / (output.width / 2)
            
            for t in [p / 100 for p in range(0, end * 100, 1)]:
                coord_x = self.x + t * math.cos(angle)
                coord_y = self.y + t * math.sin(angle)
                
                output.draw_point(int(coord_x * self.world.cell_width), 
                                  int(coord_y * self.world.cell_height), 
                                  160, 160, 160)
                          
                if not self.world.is_empty(coord_x, coord_y):
                    column_height = int(output.height // t)
                    
                    texture_id = int(self.world.scheme[int(coord_x) + int(coord_y) * self.world.width])
                    
                    if texture_id >= self.world.texture_count:
                        raise ValueError(f"Unknown texture id: {texture_id} out of {self.texture_count}")
                    
                    output.draw_recatangle(output.width // 2 + int(i),
                                           int(output.height // 2 - column_height // 2),
                                           1, column_height,
                                           self.world.pixmap.getpixel((texture_id * self.world.texture_size, 0)))
                
                    break
    
    

class Gradient(Drawable):
    
    def __init__(self):
        pass
    
    def draw(self, output):
        for j in range(output.height):
            for i in range(output.width):
                r = int(255 * j / output.height)
                g = int(255 * i / output.width)
                b = 0
                
                output.draw_point(i, j, r, g, b)
                
                
class Map(Drawable):

    def __init__(self, map_file: str):
        logging.debug("Loading map...")
        self.width, self.height, self.scheme = self._read_map(map_file)
        if len(self.scheme) != self.width * self.height:
            raise AttributeError(f"Scheme dimentions differ from {self.width} * {self.height}")
            
        logging.debug("Loading textures...")
        img = Image.open("resourses\walltext.png")
        self.pixmap = img.convert('RGB')
        self.texture_size = img.size[1]
        self.texture_count = img.size[0] / self.texture_size
        
        self.drawables = []            
        
        
    def draw(self, output) -> None:
        self.cell_width = output.width // (self.width * 2)
        self.cell_height = output.height // self.height
        
        for y in range(self.height):
            for x in range(self.width):
                if self.scheme[x + y * self.width] == " ":
                    continue
                
                rectangle_x = x * self.cell_width
                rectangle_y = y * self.cell_height
                
                texture_id = int(self.scheme[x + y * self.width])
                
                if texture_id >= self.texture_count:
                    raise ValueError(f"Unknown texture id: {texture_id} out of {self.texture_count}")
                
                output.draw_recatangle(rectangle_x, rectangle_y, 
                                       self.cell_width, self.cell_height, 
                                       self.pixmap.getpixel((texture_id * self.texture_size, 0)))
                
        for drawable in self.drawables:
            drawable.draw(output)
        
        
    def add(self, obj: Drawable) -> None:
        obj.world = self
        self.drawables.append(obj)
        
       
    def is_empty(self, x, y):
        return self.scheme[int(x) + int(y) * self.width] == " "
        
        
    def _read_map(self, filename: str) -> (int, int, str):
        with open(filename, "r") as map_file:
            lines = map_file.read().splitlines()
            
        width = len(lines[0])
        height = len(lines)
        scheme = "".join(lines)
            
        return width, height, scheme
        
    
    def _print_debug(self) -> None:
        for i in range(self.height):
            logging.debug(self.scheme[i * self.width:i * self.width + self.width])
    