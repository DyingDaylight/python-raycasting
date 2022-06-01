import unittest
import array

from image import PPMImage

class TestPPMImage(unittest.TestCase):

    def test_drawing(self):        
        expected_empty_list = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,]
        
        expected_rectangle_list = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,]
        
        expected_rectangle_with_dot_list = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,]
        
        image = PPMImage(10, 10)
        
        expected_array = array.array('B', expected_empty_list)        
        self.assertEqual(expected_array, image.framebuffer)

        expected_array = array.array('B', expected_rectangle_list)    
        image.draw_recatangle(1, 1, 8, 8, (0, 255, 0))
        self.assertEqual(expected_array, image.framebuffer)
        
        expected_array = array.array('B', expected_rectangle_with_dot_list)   
        image.draw_point(5, 5, (255, 0, 0))
        self.assertEqual(expected_array, image.framebuffer)
        
        expected_data_bytearray = bytes(expected_array)
        expected_bytearray =  bytearray("P6\n10 10\n255\n", 'ascii') + expected_data_bytearray
        
        self.assertEqual(expected_bytearray, image.get_bytes())
        self.assertEqual(expected_data_bytearray, image.get_bytes_without_header())
        
        image.flush()
        expected_array = array.array('B', expected_empty_list)        
        self.assertEqual(expected_array, image.framebuffer)
        
    def test_draw_point_invalid_color(self):
        image = PPMImage(10, 10)
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_point(0, 0, (255, 255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Color should be three component tuple of ints 0-255")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_point(0, 0, (255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Color should be three component tuple of ints 0-255")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_point(0, 0, (256, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Color should be three component tuple of ints 0-255")
        
        
    def test_draw_point_invalid_coordinates(self):
        image = PPMImage(10, 10)
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_point(10, 10, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid coordinates (10, 10)")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_point(0, 10, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid coordinates (0, 10)")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_point(10, 0, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid coordinates (10, 0)")


    def test_draw_rectangle_invalid_color(self):
        image = PPMImage(10, 10)
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 0, 8, 8, (255, 255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Color should be three component tuple of ints 0-255")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 0, 8, 8, (255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Color should be three component tuple of ints 0-255")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 0, 8, 8, (256, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Color should be three component tuple of ints 0-255")
        
    def test_draw_rectangle_invalid_coordinate(self):
        image = PPMImage(10, 10)
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(10, 10, 8, 8, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid coordinates (10, 10)")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 10, 8, 8, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid coordinates (0, 10)")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(10, 0, 8, 8, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid coordinates (10, 0)")
        
    def test_draw_rectangle_invalid_dimentions(self):
        image = PPMImage(10, 10)
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 0, 11, 8, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid dimentions (0 + 11, 0 + 8) out of 10 x 10")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 0, 8, 11, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid dimentions (0 + 8, 0 + 11) out of 10 x 10")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(5, 0, 8, 8, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid dimentions (5 + 8, 0 + 8) out of 10 x 10")
        
        with self.assertRaises(ValueError) as cntx_mngr:
            image.draw_recatangle(0, 5, 8, 8, (255, 255, 255))
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid dimentions (0 + 8, 5 + 8) out of 10 x 10")
		
if __name__ == '__main__':
    unittest.main()