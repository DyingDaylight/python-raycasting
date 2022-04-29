import sys
import logging
import math
import argparse

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QPainter

from drawables import Gradient, Map, Player
from images.image import Image

class MainWindow(QMainWindow):
    
    def __init__(self, canvas):
        super().__init__()

        self.label = QLabel()
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        

class ImageLabel(QMainWindow):

    def __init__(self):
        super().__init__()
        
        #self.setGeometry(300, 300, 250, 150)
        #self.setWindowTitle("Ray Casting")
        
        self.label = QLabel()
        
        canvas = QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        
        painter = QPainter(canvas)
        painter.drawLine(10, 10, 300, 200)
        painter.end()
        
        #pixels = [255, 0, 255] * (100 * 100)
        #logging.debug(bytes(pixels))
        
        #pixmap.loadFromData(bytes(pixels))
        #self.setPixmap(pixmap)

def main():
    parser = argparse.ArgumentParser(description="Ray casting implemention in Python.")
    parser.add_argument("-g", "--gui", help="show gui", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    
    width = 1024
    height = 512
    
    world = Map("map.txt")
    
    player = Player(3.456, 2.345)
    world.add(player)
    
    if args.gui:
        logging.debug("Start Gui")
        app = QApplication(sys.argv)
    else:
        logging.debug("Run in batch")    
        
    output = Image.get_image(width, height, args.gui)
    output.render(Gradient())
    output.render(world)

   
    if args.gui:
        window = MainWindow(output.pixmap)
        window.show()
        sys.exit(app.exec())
    else:
        output.drop("output.ppm")

    
    """        
    for frame in range(10):
        name = f"output/frame{frame}"
        player.a += 2 * math.pi / 360
        output.flush()
        output.render(world)
        output.render(player)
        output.drop(name)
    """
    
    
if __name__ == "__main__":
    main()
    
    
"""
# Choose: 2d (map), 3d (game), both
"""