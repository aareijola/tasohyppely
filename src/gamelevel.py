from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QBrush, QColor, QColorConstants, QPen, QPixmap
from characters import Character, Goal, Player, Spike
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene
import psykoosi

class GameLevel():
    """
    A class that has all the information of a single level. Can be saved to a file and opened. 
    """

    def __init__(self):
        self.name = "Default"
        self.characters = []
        self.spawn = None
        self.finish = None
        self.coins = []
        self.objects = []
        
    def setFinish(self, point):
        self.finish = point
    
    def setName(self, name):
        self.name = name

    def setSpawn(self, point):
        self.spawn = point
    
    def isPlayable(self):
        if self.spawn is not None and self.finish is not None:
            return True
        else:
            return False

    
    def generateScene(self):
        '''
        Called every time we wish to start a new game in this level. Returns a QGraphicsScene with all level information
        '''
        scene = QGraphicsScene()
        self.player = Player()
        scene.addItem(self.player)
        if self.isPlayable():
            self.player.moveBy(self.spawn.x(), self.spawn.y())
        scene.setBackgroundBrush(QBrush(QPixmap(psykoosi.BACKGROUND)))
        
        if self.finish:
            finish = Goal()
            finish.moveBy(self.finish.x() - Character.CHARSIZE / 2, self.finish.y() - Character.CHARSIZE / 2)
            scene.addItem(finish)


        brush = QBrush(QColor(128, 64, 0))
        pen = QPen()
        pen.setWidth(3)
        
        for coin in self.coins:
            scene.addItem(coin)
            coin.moveBy(coin.startX, coin.startY)
        
        for item in self.objects:
            if type(item) is QGraphicsRectItem:
                item.setBrush(brush)
                item.setPen(pen)
                scene.addItem(item)
            elif type(item) is Spike:
                scene.addItem(item)
                item.moveBy(item.startX, item.startY)
                #item.setscePos(item.startX, item.startY)
        
        for character in self.characters:
            scene.addItem(character)
            character.setPos(character.trajectory[0])
        
        

        return scene