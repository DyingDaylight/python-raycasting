import math


class Player:
    
    def __init__(self, x: int, y: int) -> None:
        # player's position
        self.x = x
        self.y = y
        
        # player's view direction
        self.a = 1.523
        self.fov = math.pi / 3
        
        # playes's size
        self.width = 5
        self.height = 5
        
        self.color = (160, 160, 160)
        
        
class Sprite:
    
    def __init__(self, x: float, y: float, texture_id: int = -1) -> None:
        self.x = x
        self.y = y
        
        self.width = 6
        self.height = 6
        
        self.texture_id = int(texture_id)
        self.texture = None
        
        self.player_distance = 0
        
    def get_color(self, u: int, v: int) -> tuple:
        if not self.texture:
            return (0, 0, 0, 255)
        
        if self.texture_id == -1:
            raise ValueError("Texture Id is not set")
        
        return self.texture.get_pixel(self.texture_id, u * self.texture.size, v * self.texture.size)
        
    def __eq__(self, other):
        return type(self) == type(other) and \
               self.x == other.x and \
               self.y == other.y and \
               self.texture_id == other.texture_id
        
        
    def __str__(self):
        return f"Sprite at ({self.x}, {self.y}) with texture {self.texture_id}"