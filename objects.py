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