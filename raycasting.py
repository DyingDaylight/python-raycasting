import sys
import logging
import math
import argparse
import time
import array

from random import randrange

from PySide6.QtCore import Qt, QPoint, QTimer, QRunnable, QThreadPool, QByteArray
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap, QPainter, QColor

from drawables import Gradient, Map, Player
from images.image import PPMImage

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
        
    output = PPMImage(width, height)
    output.render(Gradient())
    output.render(world)
    
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