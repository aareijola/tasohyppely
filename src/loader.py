from os import listdir
from characters import Coin, Enemy, Spike
from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtWidgets import QGraphicsRectItem
from gamelevel import GameLevel

def loadLevel(levelname) -> GameLevel:
    level = GameLevel()
    try:
        f = open('levels/' +(levelname) + '.txt', 'r')
        for line in f:
            text = line[5:].rstrip()
            prefix = line[0:5]
            if prefix == 'NAME:':
                level.setName(text)
            elif prefix == 'SPWN:':
                coords = text.split(',')
                level.setSpawn(QPointF(float(coords[0]), float(coords[1])))
            elif prefix == 'GOAL:':
                coords = text.split(',')
                level.setFinish(QPointF(float(coords[0]), float(coords[1])))  
            elif prefix == 'OBJCT':
                coords = text.split(',') # x, y, w, h
                level.objects.append(QGraphicsRectItem(float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])))
            elif prefix == 'COIN:':
                coords = text.split(',')
                level.coins.append(Coin(float(coords[0]), float(coords[1])))
            elif prefix == 'SPIKE':
                coords = text.split(',')
                level.objects.append(Spike(float(coords[0]), float(coords[1])))
            elif prefix == 'ENEMY':
                coordtexts = text.split(';')
                newEnemy = Enemy()
                traj = []
                for coord in coordtexts:
                    try:
                        x, y = coord.split(',')
                        point = QPointF(float(x), float(y))
                        traj.append(point)
                    except ValueError:
                        pass
                if len(traj) > 1: # We dont want to add a broken enemy to the game
                    newEnemy.setTrajectory(traj)
                    level.characters.append(newEnemy)
            else:
                pass
        f.close()
        return level
    except OSError:
        return None


def saveLevel(level) -> bool:
    """
    Saves the level to file and returns True on success, False on fail
    """
    try:
        if level.name == 'Default':
            return False
        f = open('levels/'+ level.name + '.txt', 'w')
        f.write("NAME:" + level.name + '\n')
        spawntext = "SPWN:{},{}\n".format(level.spawn.x(), level.spawn.y())
        f.write(spawntext)
    
        for item in level.objects:
            if type(item) is QGraphicsRectItem:
                f.write('OBJCT' + '{},{},{},{}\n'.format(
                    item.rect().x(),
                    item.rect().y(),
                    item.rect().width(),
                    item.rect().height()
                ))
            elif type(item) is Spike:
                f.write('SPIKE' + '{},{}\n'.format(item.startX, item.startY))

        for coin in level.coins:
            f.write('COIN:' + '{},{}\n'.format(
                coin.startX,
                coin.startY
            ))
        
        for character in level.characters:
            f.write('ENEMY')
            for coordinate in character.trajectory:
                f.write('{},{};'.format(coordinate.x(), coordinate.y()))
            f.write('\n')
            

        
        f.write("GOAL:{},{}\n".format(level.finish.x(), level.finish.y()))
        
        
        f.close()
        return True
    except OSError:
        return False

def listLevels():
    """
    This function lists simply lists all files in the levels/ directory.
    """
    levels = listdir('levels/')
    ret = []
    for level in levels:
        ret.append(level[:-4])

    return ret
