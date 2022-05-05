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
    
    def __init__(self, x: float, y: float, texture_id: int) -> None:
        self.x = x
        self.y = y
        
        self.width = 6
        self.height = 6
        
        self.texture_id = int(texture_id)
        
    def __str__(self):
        return f"Sprite at ({self.x}, {self.y}) with texture {self.texture_id}"