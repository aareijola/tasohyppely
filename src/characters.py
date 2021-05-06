from PyQt5.QtCore import QPointF, QRectF
from characterphysics import CharacterPhysics
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsPolygonItem, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor, QColorConstants, QPen, QPixmap, QPolygonF


class Character(QGraphicsRectItem):

    CHARSIZE = 64
    WORLDFLOOR = 1000

    def __init__(self):
        super().__init__(0,0, Character.CHARSIZE, Character.CHARSIZE)
        pen = QPen()
        self.dead = False
        pen.setWidth(3)
        self.setPen(pen)
        self.phys = CharacterPhysics()
        self.coins = 0

    def checkForGround(self):
        '''
        Moves player model down by 3 and checks for collisions. If colliding then it's on solid ground.
        '''
        self.moveBy(0, 3)
        if len(self.collidingItems()) > 0:
            self.phys.falling = False
        else:
            self.phys.falling = True
        self.moveBy(0, -3)
    
    def checkCollisions(self):
        """
        This method handles execution of collision methods for different characters and custom objects.
        """
        collisions = self.collidingItems()
        for item in collisions:
            self.collide(item)
        return collisions
    
    def dothemove(self):
        """
        Called periodically every game tick to move the character to their next location based on not so advanced physics.
        """
        dx, dy = self.phys.getPosDelta()
        # Move on x-axis if possible
        # Main principle for collision detection in the game is that we try to move and if we collide we cancel the move.
        self.moveBy(dx, 0)
        collisions = self.checkCollisions()
        if len(collisions) > 0:
            self.moveBy(-dx, 0)
        
        if dy == 0 and not dx == 0:  # No need to check for solid ground if not moving along x-axis
            self.checkForGround()
        
        # Move on y-axis if possible
        self.moveBy(0, dy)
        collisions = self.checkCollisions()
        while len(collisions) > 0: # Maybe implement binary search here?
            if type(collisions[0]) is not Coin:
                self.phys.collision()
            self.moveBy(0, -dy) # if a collision happens move back to the last good spot and
            dy = 0.99*dy    # try to find a smaller dy that moves reasonably close
            self.moveBy(0, dy)
            collisions = self.checkCollisions()
        
        if self.y() > self.WORLDFLOOR:
            self.dead = True

# The following declarations are done here because later classes need to know they exist

class Player(Character): 
    pass 
class Goal(QGraphicsRectItem):
    pass
class Coin(QGraphicsEllipseItem):
    pass

class Spike(QGraphicsPolygonItem):
    pass
#

class Enemy(Character):

    ENEMYSPEED = 0.5

    def __init__(self):
        super().__init__()
        self.phys = CharacterPhysics(coef = Enemy.ENEMYSPEED)
        self.setBrush(QBrush(QPixmap("data/enemy.png")))
        self.trajectory = []
        self.target = QPointF(self.scenePos())
        self.pointindex = 0

    def setTrajectory(self, points):
        self.trajectory = points
        self.target = self.trajectory[0]
        self.pointindex = 0
    
    def dothemove(self):
        """
        For enemies we add the logic to interact with waypoints to the moving sequence.
        Moving status is updated before movement the same way that keyboard input works for the player. 
        """
        if self.dead:
            self.hide()
        
        if self.contains(self.mapFromScene(QPointF(self.target.x(), self.y()))):
            if self.pointindex == len(self.trajectory) - 1:
                self.trajectory.reverse()
                self.pointindex = 0
            else:
                self.target = self.trajectory[self.pointindex + 1]
                self.pointindex += 1
        
        if self.target.x() > self.scenePos().x():
            self.phys.movingright = True
            self.phys.movingleft = False
        elif self.target.x() < self.scenePos().x():
            self.phys.movingright = False
            self.phys.movingleft = True
        
        super().dothemove()

    def collide(self, obstacle):
        if type(obstacle) is Player:
            obstacle.dead = True
        elif type(obstacle) is Enemy:
            self.trajectory.reverse()
            self.pointindex =  0


class Player(Character):

    def __init__(self):
        super().__init__()
        self.setBrush(QBrush(QPixmap("data/player.png")))
        self.atFinish = False

    def dothemove(self):
        """
        Sets atFinish boolean to false because the game would have already ended on last tick if it had been eligible. If still at
        finish on this gametick then the boolean will be set to True in time for the next level completion check in the game module.
        """
        
        if self.atFinish:
            self.atFinish = False
        
        return super().dothemove()

    def collide(self, obstacle):
        if type(obstacle) in [Enemy, Coin, Spike]:
            obstacle.collide(self)
        
        if type(obstacle) is Goal:
            self.atFinish = True



class Coin(QGraphicsEllipseItem):
    """
    For coins (and spikes) we cannot spawn them immediately at the desired x,y coords because that would mess up the pixmap.
    Therefore we have to spawn at 0,0 in their own coordinate system and then move when we add the coin to the scene. 
    """

    def __init__(self, x, y):
        super().__init__(QRectF(0, 0,Character.CHARSIZE, Character.CHARSIZE))
        self.setBrush(QBrush(QPixmap('data/coin.png')))
        self.startX = x
        self.startY = y

    def collide(self, obstacle):
        if type(obstacle) is Player:
            obstacle.coins += 1
            self.hide()

class Goal(QGraphicsRectItem):

    def __init__(self):
        super().__init__(0, 0, Character.CHARSIZE, Character.CHARSIZE)
        self.setBrush(QBrush(QPixmap('data/finish.png')))


class Spike(QGraphicsPolygonItem):

    def __init__(self, x, y):
        triangle = QPolygonF()
        sz = Character.CHARSIZE
        triangle.append(QPointF(- sz / 2,0))
        triangle.append(QPointF(0,-sz))
        triangle.append(QPointF(sz / 2,0))   
        super().__init__(triangle)
        self.setBrush(QBrush(QColor(QColorConstants.DarkGray)))
        pen = QPen()
        pen.setWidth(3)
        self.setPen(pen)
        self.startX = x
        self.startY = y

    def collide(self, obstacle):
        if type(obstacle) is Player:
            obstacle.dead = True


class Camera(QGraphicsRectItem):
    """
    This  class is a dummy item that is spawned in the level editor to give the player gameplay-like movement.
    """
    CAMERASPEED = 15
    
    def __init__(self):
        super().__init__(0,0,64,64)
        self.setBrush(QBrush(QColor(0,0,0,0)))
        #self.setPen(QPen(QColor(0,0,0,0)))
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

    def update(self):
        spd = Camera.CAMERASPEED
        if self.movingLeft:
            self.moveBy(-spd, 0)
        if self.movingRight:
            self.moveBy(spd, 0)
        if self.movingUp:
            self.moveBy(0, -spd)
        if self.movingDown:
            self.moveBy(0, spd)