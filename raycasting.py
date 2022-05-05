import argparse
import logging
import math
import io

from PIL import Image

import resources
from image import PPMImage
from objects import Player


def render(buffer, world, player, sprites, draw_map=True):
    cell_width = buffer.width // (world.width * 2) if draw_map else buffer.width // world.width
    cell_height = buffer.height // world.height
    
    if draw_map:
        # render top-down map        
        for y in range(world.height):
            for x in range(world.width):
                texture_id = world.get_texture_id(x, y)
                
                if texture_id < 0:
                    continue
                
                rectangle_x = x * cell_width
                rectangle_y = y * cell_height
                
                buffer.draw_recatangle(rectangle_x, rectangle_y, 
                                       cell_width, cell_height, 
                                       world.walls_textures.get_pixel(texture_id, 0, 0))
        
        # render player on top-down map
        buffer.draw_recatangle(int(player.x * cell_width), 
                               int(player.y * cell_height), 
                               player.width, player.height, 
                               player.color)

    working_width = buffer.width // 2 if draw_map else buffer.width
            
    # world's diagonal, the longest ray
    diagonal = int(math.sqrt(world.width ** 2 + world.height ** 2))
        
    for i in range(working_width):
        angle = player.a - player.fov / 2 + player.fov * i / working_width
           
        # iterate along the ray with 0.01 step
        for t in [p / 100 for p in range(diagonal * 100)]:
            coord_x = player.x + t * math.cos(angle)
            coord_y = player.y + t * math.sin(angle)
                
            if draw_map:
                # draw a visibility cone
                pixel_x = int(coord_x * cell_width)
                pixel_y = int(coord_y * cell_height)
                
                buffer.draw_point(pixel_x, pixel_y, player.color)
                      
            if not world.is_empty(int(coord_x), int(coord_y)):
                # visible column height depending on the distance
                column_height = int(buffer.height // (t * math.cos(angle - player.a)))
                
                texture_id = world.get_texture_id(int(coord_x), int(coord_y))
                
                hit_x = coord_x - math.floor(coord_x + 0.5) # get fractional part
                hit_y = coord_y - math.floor(coord_y + 0.5)
                
                # coordinate x inside "horizontal" texture
                texture_coord_x = hit_x * world.walls_textures.size
                if abs(hit_y) > abs(hit_x):
                    # coordinate x inside "vertical (hitx close to 0)" texture
                    texture_coord_x = hit_y * world.walls_textures.size
                
                if texture_coord_x < 0: 
                    texture_coord_x += world.walls_textures.size
                
                if not 0 <= texture_coord_x < int(world.walls_textures.size):
                    raise ValueError(f"Texture coordinate {texture_coord_x} out of range 0 - {self.world.texture_size}")
                    
                column = world.walls_textures.get_column(texture_id, texture_coord_x, column_height)

                x = working_width + int(i) if draw_map else int(i)
                for j in range(column_height):
                    y = j + int(buffer.height // 2 - column_height // 2)
                    if y < 0 or y > buffer.height:
                        continue
                    buffer.draw_point(x, y, column[j])
            
                break
                
    for sprite in sprites:
        logging.debug(f"Sprite: {sprite}")
        if draw_map:
            # draw sprite on mini map
            buffer.draw_recatangle(int(sprite.x * cell_width - sprite.width // 2), int(sprite.y * cell_height - sprite.height // 2),
                                   sprite.width, sprite.height, (255, 0, 0))

        # absolute direction from the player to the sprite
        sprite_direction = math.atan2(sprite.y - player.y, sprite.x - player.x)
        while sprite_direction - player.a >  math.pi: sprite_direction -= 2 * math.pi
        while sprite_direction - player.a < -math.pi: sprite_direction += 2 * math.pi
        
        sprite_distance = math.sqrt(pow(player.x - sprite.x, 2) + pow(player.y - sprite.y, 2))
        sprite_screen_size = int(min(2000, buffer.height // sprite_distance))
        h_offest = (sprite_direction - player.a) * working_width // player.fov + working_width // 2 - sprite_screen_size // 2
        v_offset = buffer.height // 2 - sprite_screen_size // 2
        
        for i in range(sprite_screen_size):
            if h_offest + i < 0 or h_offest + i >= working_width:
                continue
            for j in range(sprite_screen_size):
                if v_offset + j < 0 or v_offset + j >= buffer.height:
                    continue
                w = working_width if draw_map else 0
                buffer.draw_point(w + h_offest + i, v_offset + j, (0, 0, 0))
    
        

def main():
    # TODO: fish eye fix, animation?
    parser = argparse.ArgumentParser(description="Ray casting implemention in Python.")
    parser.add_argument("-g", "--gui", help="show gui", action="store_true")
    parser.add_argument("-m", "--map", help="show map", action="store_true")
    parser.add_argument("-a", "--anim", help="save as gif animation", action="store_true")
    parser.add_argument("-f", "--frames", help="amount of frames", type=int, default=1)
    # set resource file
    # set output file
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    
    width = 1024 if args.map else 512
    height = 512
    
    world, sprites = resources.parse("resources/resource.txt")
    player = Player(3.456, 2.345)
    
    buffer = PPMImage(width, height)
    
    if args.anim:
        images = []
        for frame in range(args.frames):
            logging.debug(f"Frame {frame}")
            player.a += 2 * math.pi / 360
            
            buffer.flush()
            render(buffer, world, player, sprites, args.map)
            
            images.append(Image.open(io.BytesIO(buffer.get_bytes())))
            
        images[0].save('output/animation.gif', save_all=True, append_images=images[1:], optimize=False, loop=0)
    else:
        render(buffer, world, player, sprites, args.map)
        buffer.write_to_file()    
    
    """  
    if args.gui:
        logging.debug("Start Gui")
        app = QApplication(sys.argv)
    else:
        logging.debug("Run in batch")    
    
      
    def run():
        def update_label(dt):
            logging.debug("Update label")
            player.a += 2 * math.pi / 360
            output.render(Gradient())
            output.render(world)
            window.updated = True
            window.update()
        
        FPS = 60
        lastFrameTime = time.time()
        while window.is_open:
    
            currentTime = time.time()
            # dt is the time delta in seconds (float).
            dt = currentTime - lastFrameTime
            lastFrameTime = currentTime
                
            update_label(dt)
        
        
            sleepTime = 1./FPS - (currentTime - lastFrameTime)
            if sleepTime > 0:
                time.sleep(sleepTime)
   
    #timer = QTimer()
    #timer.timeout.connect(update_label)
    #timer.start(10000)  # every 10,000 milliseconds

    if args.gui:
        window = MainWindow(output)
        window.show()
        
        p = ProcessRunnable(target=run, args=())
        p.start()
        
        sys.exit(app.exec())
    else:
        output.drop("output.ppm")

           
    for frame in range(10):
        name = f"output/frame{frame}"
        player.a += 2 * math.pi / 360
        output.flush()
        output.render(world)
        output.render(player)
        output.drop(name)

    """
    
import sys
import time 
from PySide6.QtCore import Qt, QPoint, QTimer, QRunnable, QThreadPool, QByteArray
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QPainter, QColor

class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


class MainWindow(QMainWindow):
    
    def __init__(self, output):
        super().__init__()

        self.output = output
        self.label = QLabel()
        pixmap = QPixmap(self.output.width, self.output.height)
        pixmap.loadFromData(self.output.get_bytes())
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)
        
        self.is_open = True
        self.updated = False

    def paintEvent(self, event):
        if self.updated:
            pixmap = QPixmap(self.output.width, self.output.height)
            pixmap.loadFromData(self.output.get_bytes())
            self.label.setPixmap(pixmap)
            self.updated = False
        
    def closeEvent(self, event):
        self.is_open = False
    
if __name__ == "__main__":
    main()