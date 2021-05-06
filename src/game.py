from loader import loadLevel
from characters import *
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QColorConstants, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene


class platformerGame():
    '''
    This class runs the game logic, keeps track of the player, the scene of the level
    '''

    def __init__(self, levelname):

        self.level = loadLevel(levelname)
        self.scene = self.level.generateScene()
        self.player = self.level.player
        self.characters = self.level.characters
        self.characters.append(self.player)

        self.collectedCoins = 0
        self.totalCoins = len(self.level.coins)
        self.paused = False
        self.gameover = False

        '''spike = Spike()
        spike.moveBy(-100, -100)
        self.scene.addItem(spike)'''


    def gameText(self):
        txt = "Taso: {}\n".format(self.level.name) + \
            "Kolikoita kerätty: {} / {}\n".format(self.collectedCoins, self.totalCoins) + \
            "Avaa valikko painamalla [ESC]"
        return txt 
    
    
    def allCoinsCollected(self):
        if self.collectedCoins == self.totalCoins:
            return True
        else:
            return False
    
    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def isPaused(self):
        return self.paused
    
    def checkCoins(self):
        self.collectedCoins = self.player.coins
    
    def updateGame(self):
        """
        Updates all moving characters in the scene, making them move according to their trajectories.
        Returns false as long as the game is active and True when we beat the level
        """
        if not self.gameover:
            for char in self.characters:
                char.dothemove()
            if self.player.dead:
                self.gameover = True
            self.checkCoins()

            if self.player.atFinish and self.allCoinsCollected():
                return True
        else:
            self.player.hide()
        return False


    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_A, Qt.Key_Left]:
            self.player.phys.movingleft = True
        if a0.key() in [Qt.Key_D, Qt.Key_Right]:
            self.player.phys.movingright = True
        if a0.key() in [Qt.Key_W, Qt.Key_Up]:
            self.player.phys.jump()
    
    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_A, Qt.Key_Left]:
            self.player.phys.movingleft = False
        if a0.key() in [Qt.Key_D, Qt.Key_Right]:
            self.player.phys.movingright = False

