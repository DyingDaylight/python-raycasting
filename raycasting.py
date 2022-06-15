import argparse
import logging
import math
import sys
import io

from collections import namedtuple

from PIL import Image

from PySide6.QtGui  import QPixmap, QPainter
from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition, QMutexLocker, Qt, QPointF, QElapsedTimer
from PySide6.QtWidgets import QApplication, QWidget

import resources
from image import PPMImage
from objects import Player

def render_top_bottom_map(buffer, world, world_unit: namedtuple, player, sprites):
    # render top-down map        
    for y in range(world.height):
        top_left_y = y * world_unit.height
    
        for x in range(world.width):
            if world.is_empty(x, y):
                continue
            
            top_left_x = x * world_unit.width
            
            buffer.draw_recatangle(top_left_x, top_left_y, 
                                   world_unit.width, world_unit.height, 
                                   world.get_color_from_texture(x, y, 0, 0))
    
    # render player on top-down map
    buffer.draw_recatangle(int(player.x * world_unit.width - player.width // 2), 
                           int(player.y * world_unit.height - player.height // 2), 
                           player.width, player.height, 
                           player.color)
                           
    for sprite in sprites:
        # draw sprite on mini map
        buffer.draw_recatangle(int(sprite.x * world_unit.width - sprite.width // 2), 
                               int(sprite.y * world_unit.height - sprite.height // 2),
                               sprite.width, sprite.height, 
                               (255, 0, 0))
    


def render(buffer, world, player, sprites, draw_map=True):
    cell_width = buffer.width // (world.width * 2) if draw_map else buffer.width // world.width
    cell_height = buffer.height // world.height

    working_width = buffer.width // 2 if draw_map else buffer.width
    depth_cache = [1000 for i in range(working_width)]
            
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
                distance = t * math.cos(angle - player.a)
                depth_cache[i] = distance
                column_height = int(buffer.height // distance)
                
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
                
    if draw_map:
        WorldUnit = namedtuple('WorldUnit', 'width height')
        wu = WorldUnit(cell_width, cell_height)
        render_top_bottom_map(buffer, world, wu, player, sprites)
           
    # TODO replace with depth cache
    for sprite in sprites:
        sprite.player_distance = math.sqrt(pow(player.x - sprite.x, 2) + pow(player.y - sprite.y, 2))
                
    sprites.sort(key=lambda s: s.player_distance, reverse=True)
                
    for sprite in sprites:
        # absolute direction from the player to the sprite
        sprite_direction = math.atan2(sprite.y - player.y, sprite.x - player.x)
        while sprite_direction - player.a >  math.pi: sprite_direction -= 2 * math.pi
        while sprite_direction - player.a < -math.pi: sprite_direction += 2 * math.pi
        
        sprite_screen_size = int(min(2000, buffer.height // sprite.player_distance))
        h_offest = int((sprite_direction - player.a) / player.fov * working_width + working_width / 2 - sprite_screen_size / 2)
        v_offset = buffer.height // 2 - sprite_screen_size // 2
        
        for i in range(sprite_screen_size):
            if h_offest + i < 0 or h_offest + i >= working_width:
                continue
            if depth_cache[int(h_offest + i)] < sprite.player_distance:
                continue
            for j in range(sprite_screen_size):
                if v_offset + j < 0 or v_offset + j >= buffer.height:
                    continue
                    
                w = working_width if draw_map else 0
                color = sprite.get_color(i / sprite_screen_size, j / sprite_screen_size)
                if color[3] > 128:
                    buffer.draw_point(w + h_offest + i, v_offset + j, color[:3])
    
class RenderThread(QThread):

    rendered_image = Signal(PPMImage)

    def __init__(self, buffer, world, player, sprites, draw_map, frames, parent=None):
        super().__init__(parent)
        
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        
        self.buffer = buffer
        self.world = world
        self.player = player
        self.sprites = sprites
        self.draw_map = draw_map
        self.frames = frames
        
        self.restart = False
        self.abort = False


    def stop(self):
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()
        
        self.wait(2000)
        
    
    def render(self):
        with QMutexLocker(self.mutex):
            if not self.isRunning():
                self.start(QThread.LowPriority)
            else:
                self.restart = True
                self.condition.wakeOne()
        
    
    def run(self):
        timer = QElapsedTimer()
        
        while True:
            current_frame = 0
            while current_frame < self.frames:
                timer.restart()
                if self.restart:
                    break
                
                if self.abort:
                    return
                    
                
                logging.debug(f"Frame: {current_frame}")
                    
                self.player.a += 2 * math.pi / 360
                
                buffer = PPMImage(self.buffer.width, self.buffer.height)
                render(buffer, self.world, self.player, self.sprites, self.draw_map)
                self.rendered_image.emit(buffer)
                
                current_frame += 1
                
            self.mutex.lock()
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()
            
    
class ImageWidget(QWidget):
    
    def __init__(self, buffer, world, player, sprites, draw_map, frames, parent=None):
        super().__init__(parent)
        
        self.thread = RenderThread(buffer, world, player, sprites, draw_map, frames)
        self.pixmap = QPixmap()
        
        self._pixmap_offset = QPointF()
        
        self.thread.rendered_image.connect(self.update_pixmap)
        
        self.setWindowTitle("Ray Casting")
        
        self.thread.render()
        
        
    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.fillRect(self.rect(), Qt.black) 
            if self.pixmap.isNull():
                loading_text = "Loading..."
                metrics = painter.fontMetrics()
                text_width = metrics.horizontalAdvance(loading_text)
                painter.setPen(Qt.white)
                painter.drawText((self.width() - text_width) / 2, metrics.leading() + metrics.ascent(), loading_text)
            else:
                painter.drawPixmap(self._pixmap_offset, self.pixmap)
        
        
    def update_pixmap(self, image):
        self.pixmap = QPixmap(image.width, image.height)
        self.pixmap.loadFromData(image.get_bytes())
        self.update()
    

def main(line_args=None):    
    parser = argparse.ArgumentParser(description="Ray casting implemention in Python.")
    parser.add_argument("-g", "--gui", help="show gui", action="store_true")
    parser.add_argument("-m", "--map", help="show map", action="store_true")
    parser.add_argument("-a", "--angle", help="Player's view angle", type=float, default=1.523)
    parser.add_argument("-f", "--frames", help="amount of frames", type=int, default=1)
    parser.add_argument("-o", "--output", help="path to output file", type=str, default="output\output")
    # set resource file
    if line_args:
        args = parser.parse_args(line_args)
    else:
        args = parser.parse_args()
        
    print(args.output)
    
    name = args.output if args.output else "output/output"

    logging.basicConfig(level=logging.DEBUG)
    
    width = 1024 if args.map else 512
    height = 512
    
    world, sprites = resources.parse("resources/resource.txt")
    player = Player(3.456, 2.345)
    
    buffer = PPMImage(width, height) 
    
    if args.gui:
        logging.debug("Start Gui")
        app = QApplication(sys.argv) 
        widget = ImageWidget(buffer, world, player, sprites, args.map, args.frames)
        widget.resize(width, height)
        widget.show()
        code = app.exec()
        widget.thread.stop()
        sys.exit(code)
    else:
        if args.frames > 1:
            images = []
            for frame in range(args.frames):
                logging.debug(f"Frame {frame}")
                player.a += 2 * math.pi / 360
                
                buffer.flush()
                render(buffer, world, player, sprites, args.map)
                
                images.append(Image.open(io.BytesIO(buffer.get_bytes())))
                
            if not name.endswith('.gif'): name += ".gif"
            images[0].save(name, save_all=True, append_images=images[1:], optimize=False, loop=0)
        else:
            render(buffer, world, player, sprites, args.map)
            buffer.write_to_file(name)   
        
        
if __name__ == "__main__":    
    main()