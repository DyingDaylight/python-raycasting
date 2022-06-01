import unittest
import resources
from image import PPMImage
from objects import Player

from collections import namedtuple
from raycasting import render_top_bottom_map

class TestRenderMap(unittest.TestCase):

    def test_render_top_bottom_map(self):
        world, sprites = resources.parse("test_resources/resources/map_only.txt")
        player = Player(3.456, 2.345)
        
        buffer = PPMImage(192, 192) # 32 * world.width, 32 * world.height
        WorldUnit = namedtuple('WorldUnit', 'width height')
        wu = WorldUnit(32, 32)
        
        render_top_bottom_map(buffer, world, wu, player, sprites)
        
        #buffer.write_to_file("test_resources/expected/map_only.ppm")
        
        with open("test_resources/expected/map_only.ppm", "rb") as f:
            c = f.read()
            self.assertEqual(c, buffer.get_bytes())       
        
        
if __name__ == '__main__':
    unittest.main()