import logging
import os

from PIL import Image

from objects import Sprite


def parse(filename: str) -> tuple:
    logging.debug(f"Loading resources from {filename}...")
    
    if not os.path.exists(filename):
        raise AttributeError(f"Resource file {filename} is not found.")
        
    sprites = []
    enemies_textures = None
        
    with open(filename, "r") as resource_file:
        lines = resource_file.read().splitlines()
        
    for i, line in enumerate(lines):
        if line.startswith("walls_textures"):
            logging.debug("Loading walls' textures...")
            
            texture_filename = line.split(":")[1]
            
            if not os.path.exists(texture_filename):
                raise AttributeError(f"Texture file {texture_filename} is not found.")
        
            image = Image.open(texture_filename)
            pixmap = image.convert('RGB')
            walls_textures = Texture(pixmap)
            
        if line.startswith("enemies:"):
            logging.debug("Loading enemies...")
            
            enenmies_data = line.split(":")[1].split(";")
            sprites = [Sprite(*tuple(map(float, data.split(",")))) for data in enenmies_data]
        
        if line.startswith("enemies_textures"):
            logging.debug("Loading enemies' textures...")
            
            enenmies_filename = line.split(":")[1]
            
            if not os.path.exists(enenmies_filename):
                raise AttributeError(f"Texture file {enenmies_filename} is not found.")
            
            # TODO: parse sprites
            image = Image.open(enenmies_filename)
            pixmap = image.convert('RGBA')
            enemies_textures = Texture(pixmap)
            
        if line.startswith("map_scheme"):
            logging.debug("Parsing world map...")
            
            width = len(lines[i + 1])
            height = len(lines) - i - 1
            scheme = "".join(lines[i + 1:])
            
            if len(scheme) != width * height:
                raise AttributeError(f"World dimentions {len(scheme)} differ from {width} * {height}")
            
            world = World(width, height, scheme, walls_textures)
            break
            
    if enemies_textures:
        for sprite in sprites:
            sprite.texture = enemies_textures
        
    return world, sprites
    
    
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
            raise ValueError("Wrong texture id")

        if x_in_texture < 0 or x_in_texture >= self.size:
            raise ValueError("x out of range")
            
        #if height > self.size:
        #    raise ValueError("Desired height is more that size")
            
        column = []
        
        for y in range(height):
            pixel_x = texture_id * self.size + x_in_texture
            pixel_y = int((y * self.size) / height)
            column.append(self.pixmap.getpixel((pixel_x, pixel_y)))
                
        return column    
        
    
    def get_pixel(self, texture_id: int, x: int, y: int) -> tuple:
        return self.pixmap.getpixel((x + texture_id * self.size, y))
        
    
class World:
    
    def __init__(self, width: int, height: int, scheme: str, walls_textures: Texture) -> None:
        self.width = width
        self.height = height
        self.scheme = scheme
        self.walls_textures = walls_textures
        
    
    def is_empty(self, x: int, y: int) -> bool:
        return self.scheme[x + y * self.width] == " "
        
        
    def get_texture_id(self, x: int, y: int) -> int:
        char = self.scheme[x + y * self.width]
        if char == " ":
            return -1
        
        texture_id = int(char)
        
        if texture_id >= self.walls_textures.count:
            raise ValueError(f"Unknown texture id: {texture_id} out of {self.walls_textures.count}")
            
        return texture_id
        
        
    def _print_debug(self) -> None:
        for i in range(self.height):
            logging.debug(self.scheme[i * self.width:i * self.width + self.width])