import logging
import random
import os

from PIL import Image

from objects import Sprite


def parse(filename: str) -> tuple:
    logging.debug(f"Loading resources from {filename}...")
    
    if not os.path.exists(filename):
        raise AttributeError(f"Resource file {filename} is not found.")
        
    enemies = []
    enemies_textures = None
    walls_textures = None
        
    with open(filename, "r") as resource_file:
        text = resource_file.read()
        if "map_scheme:" not in text:
            raise ValueError("Map scheme is not provided")
        lines = text.splitlines()
                
    for i, line in enumerate(lines):            
        if line.startswith("enemies:"):
            logging.debug("Loading enemies...")
            
            enenmies_data = line.split(":")[1].split(";")
            enemies = [Sprite(*tuple(map(float, data.split(",")))) for data in enenmies_data]
        
        if line.startswith("enemies_textures") and enemies:
            logging.debug("Loading enemies' textures...")
            
            enenmies_filename = line.split(":")[1]
            
            if not os.path.exists(enenmies_filename):
                raise AttributeError(f"Texture file {enenmies_filename} is not found.")
            
            # TODO: parse sprites
            image = Image.open(enenmies_filename)
            pixmap = image.convert('RGBA')
            enemies_textures = Texture(pixmap)
            
        if line.startswith("walls_textures"):
            logging.debug("Loading walls' textures...")
            
            texture_filename = line.split(":")[1]
            
            if not os.path.exists(texture_filename):
                raise AttributeError(f"Texture file {texture_filename} is not found.")
        
            image = Image.open(texture_filename)
            pixmap = image.convert('RGB')
            walls_textures = Texture(pixmap)
            
        if line.startswith("map_scheme"):
            logging.debug("Parsing world map...")
            
            width = len(lines[i + 1])
            height = len(lines) - i - 1
            scheme = "".join(lines[i + 1:])
            
            if len(scheme) != width * height:
                raise AttributeError(f"World dimentions {len(scheme)} differ from {width} * {height}")
                
            for i in scheme:
                if i == " ": 
                    continue
                elif i.isdigit(): 
                    if walls_textures and (int(i) < 0 or int(i) >= walls_textures.count):
                        raise AttributeError(f"Invalid wall texture id: {i}")
                else: 
                    raise AttributeError(f"Invalid map symbol {i}")
                    
            world = World(width, height, scheme, walls_textures)
            break
            
    if enemies_textures:
        for sprite in enemies:
            sprite.texture = enemies_textures
        
    return world, enemies
    
    
class Texture:
    
    def __init__(self, pixmap: Image) -> None:
        """Texture is a number of squares in a row"""
    
        self.pixmap = pixmap
        
        self.size = pixmap.size[1]
        self.count, mod = divmod(pixmap.size[0], self.size)
        
        if mod != 0:
            raise ValueError("Textures are not squares")
        if self.size * self.count !=  self.pixmap.size[0]:
            raise ValueError("Textures are not squares")
        
    
    def get_column(self, texture_id: int, x_in_texture: float, height: int) -> list:
        if texture_id < 0 or texture_id >= self.count:
            raise ValueError("Invalid texture id")

        if x_in_texture < 0 or x_in_texture >= self.size:
            raise ValueError("x out of range")
            
        column = []
        
        for y in range(height):
            pixel_x = texture_id * self.size + x_in_texture
            pixel_y = int((y * self.size) / height)
            column.append(self.pixmap.getpixel((pixel_x, pixel_y)))
                
        return column    
        
    
    def get_pixel(self, texture_id: int, x: int, y: int) -> tuple:
        if texture_id < 0 or texture_id >= self.count:
            raise ValueError("Invalid texture id")
        if x < 0 or x >= self.size:
            raise ValueError("x out of range")
        if y < 0 or y >= self.size:
            raise ValueError("y out of range")
        return self.pixmap.getpixel((x + texture_id * self.size, y))
        
    
class World:
    
    def __init__(self, width: int, height: int, scheme: str, walls_textures: Texture) -> None:
        self.width = width
        self.height = height
        self.scheme = scheme
        self.walls_textures = walls_textures
        random.seed(666)
        if not self.walls_textures:
            self.walls_colors = {}
            max_texture_id = max(int(ch) for ch in self.scheme if ch.isdigit())
            for i in range(max_texture_id + 1):
                self.walls_colors[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    
    def is_empty(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width:
            raise ValueError("x out of range")
        if y < 0 or y >= self.width:
            raise ValueError("y out of range")
            
        return self.scheme[x + y * self.width] == " "
        
    # TODO: write tests
    def get_color_from_texture(self, x: int, y: int, u: int, v: int):
        if not self.walls_textures:
            return self.walls_colors[self.get_texture_id(x, y)]
    
        return self.walls_textures.get_pixel(self.get_texture_id(x, y), u, v)
        
        
    def get_texture_id(self, x: int, y: int) -> int:
        if x < 0 or x >= self.width:
            raise ValueError("x out of range")
        if y < 0 or y >= self.width:
            raise ValueError("y out of range")
            
        char = self.scheme[x + y * self.width]
        if char == " ":
            return -1
        
        texture_id = int(char)
        
        if self.walls_textures and texture_id >= self.walls_textures.count:
            raise ValueError(f"Unknown texture id: {texture_id} out of {self.walls_textures.count}")
            
        return texture_id
        
        
    def _print_debug(self) -> None:
        for i in range(self.height):
            logging.debug(self.scheme[i * self.width:i * self.width + self.width])