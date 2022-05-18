import unittest

from PIL import Image

from resources import Texture, World

class TestWorld(unittest.TestCase):

    def setUp(self):
        filename = "test_resources/textures/textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        texture = Texture(pixmap)
        scheme = "000001   11 2 11   100000"
        self.world = World(5, 5, scheme, texture)
        
    def test_world_is_empty(self):
        self.assertFalse(self.world.is_empty(0, 0))
        self.assertFalse(self.world.is_empty(4, 0))
        self.assertFalse(self.world.is_empty(0, 4))
        self.assertTrue(self.world.is_empty(1, 1))
        
    def test_world_is_empty_out_of_range(self):
        with self.assertRaises(ValueError, msg="x out of range"):
            self.world.is_empty(-1, 0)
        with self.assertRaises(ValueError, msg="x out of range"):
            self.world.is_empty(25, 0)
        with self.assertRaises(ValueError, msg="x out of range"):
            self.world.is_empty(26, 0)
            
        with self.assertRaises(ValueError, msg="y out of range"):
            self.world.is_empty(0, -1)
        with self.assertRaises(ValueError, msg="y out of range"):
            self.world.is_empty(0, 25)
        with self.assertRaises(ValueError, msg="y out of range"):
            self.world.is_empty(0, 26)
            
    def test_world_get_texture_id(self):
        self.assertEqual(self.world.get_texture_id(0, 0), 0)
        self.assertEqual(self.world.get_texture_id(0, 1), 1)
        self.assertEqual(self.world.get_texture_id(2, 2), 2)
        self.assertEqual(self.world.get_texture_id(1, 1), -1)
        
    def test_world_get_texture_id_out_of_range(self):
        with self.assertRaises(ValueError, msg="x out of range"):
            self.world.get_texture_id(-1, 0)
        with self.assertRaises(ValueError, msg="x out of range"):
            self.world.get_texture_id(25, 0)
        with self.assertRaises(ValueError, msg="x out of range"):
            self.world.get_texture_id(26, 0)
            
        with self.assertRaises(ValueError, msg="y out of range"):
            self.world.get_texture_id(0, -1)
        with self.assertRaises(ValueError, msg="y out of range"):
            self.world.get_texture_id(0, 25)
        with self.assertRaises(ValueError, msg="y out of range"):
            self.world.get_texture_id(0, 26)
            
    def test_world_get_texture_id_invalid_texture_id(self):
        self.world.scheme = "000001   11 3 11   100000"
        with self.assertRaises(ValueError, msg="Unknown texture id: 3 out of 3"):
            self.world.get_texture_id(2, 2)
            
    def test_logging(self):
        with self.assertNoLogs(level="INFO"):
            self.world.is_empty(0, 0)
        with self.assertNoLogs(level="INFO"):
            self.world.get_texture_id(0, 0)
            
if __name__ == '__main__':
    unittest.main()