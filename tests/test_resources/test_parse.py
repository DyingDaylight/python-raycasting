import unittest

from PIL import Image, ImageChops

from objects import Sprite
from resources import Texture, World, parse

class TestParse(unittest.TestCase):

    def test_map_only(self):
        filename = "test_resources/resources/map_only.txt"
        world, enemies = parse(filename)
        self.assertEqual(enemies, [])
        expected_scheme = "0111110    0033  00    00    0222220"
        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 6)
        self.assertEqual(world.scheme, expected_scheme)
        self.assertIsNone(world.walls_textures, None)
        
    def test_map_walls_textures_enemies_emeies_textures(self):
        filename = "test_resources/resources/map_textures_enemies_textures.txt"
        
        image = Image.open("test_resources/textures/textures.png")
        expected_pixmap = image.convert('RGB')
        expected_pixmap_with_alpha = image.convert('RGBA')
        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        diff = ImageChops.difference(world.walls_textures.pixmap, expected_pixmap)
        self.assertFalse(diff.getbbox())     
        
        self.assertEqual(enemies, [Sprite(1,1,1), Sprite(2,2,1)])
        for enemy in enemies:
            self.assertFalse(ImageChops.difference(enemy.texture.pixmap, expected_pixmap_with_alpha).getbbox())
        
    def test_map_walls_textures_enemies(self):
        filename = "test_resources/resources/map_textures_enemies.txt"
        
        image = Image.open("test_resources/textures/textures.png")
        expected_pixmap = image.convert('RGB')
        expected_pixmap_with_alpha = image.convert('RGBA')
        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        diff = ImageChops.difference(world.walls_textures.pixmap, expected_pixmap)
        self.assertFalse(diff.getbbox())     
        
        self.assertEqual(enemies, [Sprite(1,1,-1), Sprite(2,2,-1)])
        for enemy in enemies:
            self.assertIsNone(enemy.texture)
        
    def test_map_walls_textures_emeies_textures(self):
        filename = "test_resources/resources/map_textures_textures.txt"
        
        image = Image.open("test_resources/textures/textures.png")
        expected_pixmap = image.convert('RGB')
        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        diff = ImageChops.difference(world.walls_textures.pixmap, expected_pixmap)
        self.assertFalse(diff.getbbox())     
        
        self.assertEqual(enemies, [])
        
    def test_map_enemies_emeies_textures(self):
        filename = "test_resources/resources/map_enemies_textures.txt"
        
        image = Image.open("test_resources/textures/textures.png")
        expected_pixmap_with_alpha = image.convert('RGBA')
        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        self.assertIsNone(world.walls_textures) 
        
        self.assertEqual(enemies, [Sprite(1,1,1), Sprite(2,2,1)])
        for enemy in enemies:
            self.assertFalse(ImageChops.difference(enemy.texture.pixmap, expected_pixmap_with_alpha).getbbox())
        
    def test_map_and_walls_textures(self):
        filename = "test_resources/resources/map_textures.txt"
        
        image = Image.open("test_resources/textures/textures.png")
        expected_pixmap = image.convert('RGB')
        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        diff = ImageChops.difference(world.walls_textures.pixmap, expected_pixmap)
        self.assertFalse(diff.getbbox())     
        
        self.assertEqual(enemies, [])
        
    def test_map_and_enemies(self):
        filename = "test_resources/resources/map_enemies.txt"

        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        self.assertIsNone(world.walls_textures)     
        
        self.assertEqual(enemies, [Sprite(1,1,-1), Sprite(2,2,-1)])
        for enemy in enemies:
            self.assertIsNone(enemy.texture)
        
    def test_map_emeies_textures(self):
        filename = "test_resources/resources/map_e_textures.txt"
        
        image = Image.open("test_resources/textures/textures.png")
        expected_pixmap_with_alpha = image.convert('RGBA')
        expected_scheme = "0000000    00    0000000"
        
        world, enemies = parse(filename)

        self.assertEqual(world.width, 6)
        self.assertEqual(world.height, 4)
        self.assertEqual(world.scheme, expected_scheme)
        self.assertIsNone(world.walls_textures)     
        
        self.assertEqual(enemies, [])

    def test_without_map(self):
        filename = "test_resources/resources/without_map.txt"
        with self.assertRaises(ValueError) as cntx_mngr:
            world, enemies = parse(filename)
        self.assertEqual(cntx_mngr.exception.args[0], "Map scheme is not provided")
        
    def test_no_texture_for_id(self):
        filename = "test_resources/resources/invalid_texture_id.txt"
        
        with self.assertRaises(AttributeError) as cntx_mngr:
            world, enemies = parse(filename)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid wall texture id: 3")

    def test_invalid_map_scheme(self):
        filename = "test_resources/resources/invalid_map_symbol.txt"
        
        with self.assertRaises(AttributeError) as cntx_mngr:
            world, enemies = parse(filename)
        self.assertEqual(cntx_mngr.exception.args[0], "Invalid map symbol -")
        
    def test_file_does_not_exist(self):
        filename = "test_resources/resources/resource_not_exist.txt"
        
        with self.assertRaises(AttributeError) as cntx_mngr:
            world, enemies = parse(filename)
        self.assertEqual(cntx_mngr.exception.args[0], f"Resource file {filename} is not found.")
        
    def test_walls_textures_file_does_not_exist(self):
        filename = "test_resources/resources/invalid_wall_texture.txt"
        
        with self.assertRaises(AttributeError) as cntx_mngr:
            world, enemies = parse(filename)
        self.assertEqual(cntx_mngr.exception.args[0], "Texture file test_resources/textures/walls.png is not found.")
        
    def test_enemies_texture_file_does_not_exist(self):
        filename = "test_resources/resources/invalid_enemies_texture.txt"
        
        with self.assertRaises(AttributeError) as cntx_mngr:
            world, enemies = parse(filename)
        self.assertEqual(cntx_mngr.exception.args[0], "Texture file test_resources/textures/enemies.png is not found.")
        
        
if __name__ == '__main__':
    unittest.main()