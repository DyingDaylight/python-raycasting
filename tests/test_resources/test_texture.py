import unittest

from PIL import Image

from resources import Texture

class TestTexture(unittest.TestCase):
    
    def setUp(self):
        filename = "test_resources/textures/textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        self.texture = Texture(pixmap)
    
    def test_square_texture(self):
        self.assertEqual(self.texture.size, 32)
        self.assertEqual(self.texture.count, 3)
    
    def test_non_square_texture(self):
        filename = "test_resources/textures/non_square_width_textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        with self.assertRaises(ValueError) as cntx_mngr:
            texture = Texture(pixmap)
        self.assertEqual(cntx_mngr.exception.args[0], "Textures are not squares")
            
        filename = "test_resources/textures/non_square_height_textures.png"
        image = Image.open(filename)
        pixmap = image.convert('RGBA')
        with self.assertRaises(ValueError) as cntx_mngr:
            texture = Texture(pixmap)
        self.assertEqual(cntx_mngr.exception.args[0], "Textures are not squares")

    def test_get_column(self):
        expected_column = [(192, 192, 0, 255) for i in range(32)]
        column = self.texture.get_column(0, 0, self.texture.size)
        self.assertEqual(column, expected_column)
        
        expected_column = [(192, 192, 0, 255) for i in range(32)]
        column = self.texture.get_column(0, 31, self.texture.size)
        self.assertEqual(column, expected_column)
        
        expected_column = [(255, 0, 0, 255) for i in range(32)]
        column = self.texture.get_column(1, 0, self.texture.size)
        self.assertEqual(column, expected_column)
        
        expected_column = [(255, 0, 0, 255) for i in range(32)]
        expected_column[16] = (0, 255, 0, 255)
        column = self.texture.get_column(1, 16, self.texture.size)
        self.assertEqual(column, expected_column)
        
        expected_column = [(0, 0, 255, 255) for i in range(32)]
        column = self.texture.get_column(2, 16, self.texture.size)
        self.assertEqual(column, expected_column)

    def test_get_column_invalid_texture_id(self):
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_column(3, 0, self.texture.size)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid texture id")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_column(4, 0, self.texture.size)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid texture id")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_column(-1, 0, self.texture.size)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid texture id")
        
    def test_get_column_x_out_of_range(self):
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_column(1, -1, self.texture.size)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_column(0, 32, self.texture.size)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_column(0, 33, self.texture.size)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")

    def test_get_column_scaled(self):        
        height = 16
        expected_column = [(0, 0, 255, 255) for i in range(height)]
        column = self.texture.get_column(2, 0, height)
        self.assertEqual(len(column), len(expected_column))
        self.assertEqual(column, expected_column)

    def test_get_column_scale_out_of_range(self):
        height = 64
        expected_column = [(255, 0, 0, 255) for i in range(64)]
        expected_column[0] = expected_column[1] = (192, 192, 0, 255)
        expected_column[62] = expected_column[63] = (192, 192, 0, 255)
        column = self.texture.get_column(0, 1, height)
        self.assertEqual(len(column), len(expected_column))
        self.assertEqual(column, expected_column)
        
    def test_get_pixel(self):
        pixel = self.texture.get_pixel(0, 0, 0)
        self.assertEqual((192, 192, 0, 255), pixel)
        
        pixel = self.texture.get_pixel(1, 16, 16)
        self.assertEqual((0, 255, 0, 255), pixel)
        
    def test_get_pixel_invalid_texture_id(self):
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(-1, 0, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid texture id")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(3, 0, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid texture id")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(4, 0, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid texture id")
            
    def test_get_pixel_invalid_coordinate(self):
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, 32, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, 33, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, -1, 0)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")
            
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, 0, 32)
        self.assertEqual(cntx_mngr.exception.args[0], "y out of range")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, 0, 33)
        self.assertEqual(cntx_mngr.exception.args[0], "y out of range")
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, 0, -1)
        self.assertEqual(cntx_mngr.exception.args[0], "y out of range")
            
        with self.assertRaises(ValueError) as cntx_mngr:
            self.texture.get_pixel(0, 32, 32)
        self.assertEqual(cntx_mngr.exception.args[0], "x out of range")
            
    def test_logging(self):
        with self.assertNoLogs(level="INFO"):
            self.texture.get_pixel(0, 0, 0)
        with self.assertNoLogs(level="INFO"):
            self.texture.get_column(0, 0, self.texture.size)
        
if __name__ == '__main__':
    unittest.main()