import unittest
import argparse
import raycasting
import logging
import time
import math

class TestRaycasting(unittest.TestCase):

    def test_raycasting(self):
        filepath = r"test_resources/temp/result.ppm"
        
        raycasting.main([f'-m', '-o', f'{filepath}'])   
        
        with open("test_resources/expected/final_image.ppm", "rb") as f:
            expected = f.read()
            
        with open(filepath, "rb") as f:
            result = f.read()
            
        self.assertEqual(expected, result, "Image differs from expected") 


    def test_raycasting_time(self):
        filepath = r"test_resources/temp/result.ppm"
        
        angle = 0
        times = []
        for frame in range(360):
            angle += 2 * math.pi / 360
            start_time = time.time()
            raycasting.main([f'-m', '-o', f'{filepath}', '-a', f'{angle}'])   
            times.append(time.time() - start_time)
            
        logging.info(f"{len(times)} runs performed in {sum(times) / len(times)} on avarage")
        logging.info(f"Best time = {min(times)}, worst time = {max(times)}")
        
        
if __name__ == '__main__':
    unittest.main()