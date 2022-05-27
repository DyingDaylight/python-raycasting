import unittest

from PIL import Image, ImageChops

from objects import Sprite
from resources import Texture, World, parse

class TestSprite(unittest.TestCase):

    def test_get_color(self):
        sprite = Sprite(1, 1, 1)
    
        filename = "test_resources/textures/textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        sprite.texture = Texture(pixmap)
        
        color = sprite.get_color(0.5, 0.5)
        expected_color = (0, 255, 0, 255)
        self.assertEqual(expected_color, color)

    def test_get_color_without_texture(self):
        sprite = Sprite(1, 1, 0)
        
        color = sprite.get_color(0, 0)
        expected_color = (0, 0, 0, 255)
        self.assertEqual(expected_color, color)
        
    def test_get_color_invalid_texture_id_with_texture(self):
        sprite = Sprite(1, 1)
        
        filename = "test_resources/textures/textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        sprite.texture = Texture(pixmap)
        
        with self.assertRaises(ValueError) as cntx_mngr:
            color = sprite.get_color(0, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "Texture Id is not set")
        
    def test_get_color_invalid_texture_id_without_texture(self):
        sprite = Sprite(1, 1)
        
        color = sprite.get_color(0, 0)
        expected_color = (0, 0, 0, 255)
        self.assertEqual(expected_color, color)

if __name__ == '__main__':
    unittest.main()