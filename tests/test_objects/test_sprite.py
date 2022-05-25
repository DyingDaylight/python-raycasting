import unittest

from PIL import Image, ImageChops

from objects import Sprite
from resources import Texture, World, parse

class TestSprite(unittest.TestCase):

    def test_get_color(self):
        sprite = Sprite(1, 1, 0)
    
        filename = "test_resources/textures/textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        sprite.texture = Texture(pixmap)
        
        color = sprite.get_color(0, 0)

    def test_get_color_no_texture(self):
        pass
        
    def test_get_color_invalid_texture_id(self):
        pass

if __name__ == '__main__':
    unittest.main()