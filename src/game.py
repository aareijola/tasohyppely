from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene


class Game():
    '''
    This class runs the game logic ie. keeps track of the player, the scene of the level
    '''

    def __init__(self):
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QPixmap("data/background.png")))
        self.scene.setSceneRect(0, 0, 1270, 710)
        self.player = QGraphicsRectItem(100, 100, 100, 100)
        self.scene.addItem(self.player)
        self.paused = False
        self.gaming = False

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def isPaused(self):
        return self.paused
    
    def updateGame(self):
        pass

    def loadLevel(self):
        pass
