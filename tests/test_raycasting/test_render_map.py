import unittest
import resources
from image import PPMImage
from objects import Player

from collections import namedtuple
from raycasting import render_top_bottom_map

class TestRenderMap(unittest.TestCase):

    def setUp(self):
        self.player = Player(3.456, 2.345)
        
        self.buffer = PPMImage(192, 192) # 32 * world.width, 32 * world.height
        WorldUnit = namedtuple('WorldUnit', 'width height')
        self.wu = WorldUnit(32, 32)

    def test_render_top_bottom_map(self):
        filenames = ["map_only",
                    "map_textures_enemies_textures",
                    "map_textures_enemies",
                    "map_textures_textures",
                    "map_enemies_textures",
                    "map_textures",
                    "map_enemies",
                    "map_e_textures",]
                    
        for filename in filenames:
            world, sprites = resources.parse(f"test_resources/resources/{filename}.txt")
           
            render_top_bottom_map(self.buffer, world, 
                                  self.wu, self.player, 
                                  sprites)
            
            #self.buffer.write_to_file(f"test_resources/expected/{filename}.ppm")
            
            with open(f"test_resources/expected/{filename}.ppm", "rb") as f:
                c = f.read()
                self.assertEqual(c, self.buffer.get_bytes(), f"Failed to render {filename}")  
        
        
if __name__ == '__main__':
    unittest.main()