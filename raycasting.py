import logging
import math

from drawables import Gradient, Map, Player
from image import PPMImage


def main():
    logging.basicConfig(level=logging.DEBUG)
    
    world = Map(16, 16, "map.txt")
    
    player = Player(3.456, 2.345)
    world.add(player)
    
    output = PPMImage(1024, 512)
    
    for frame in range(10):
        name = f"output/frame{frame}"
        player.a += 2 * math.pi / 360
        output.flush()
        output.render(world)
        output.render(player)
        output.drop(name)
    
    
if __name__ == "__main__":
    main()
    
    
"""
# Choose: 2d (map), 3d (game), both
"""