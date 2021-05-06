import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication
from loader import *
from gamelevel import GameLevel


def main():
    global app
    app = QApplication(sys.argv)

    level = GameLevel()
    level.setName("asdasd")
    
    level.spawn = QPoint(0, 0)

    level.finish = QPoint(1000, 0)

    laatikko = QGraphicsRectItem(0, 100, 1000, 50)
    box2 = QGraphicsRectItem(500, -200, 100, 32)
    level.objects.append(laatikko)
    level.objects.append(box2)

    mob1 = Enemy()
    start = QPointF(200, 34)
    end = QPointF(500, 34)
    mob1.setTrajectory([start, end])
    level.characters.append(mob1)

    mob2 = Enemy()
    start = QPointF(600, 34)
    end = QPointF(900, 34)
    mob2.setTrajectory([start, end])
    level.characters.append(mob2)

    coin1 = Coin(300, -400)
    level.coins.append(coin1)
    coin2 = Coin(800, -400)
    level.coins.append(coin2)

    spike1 = Spike(150, 100)
    level.objects.append(spike1)


    
    print(saveLevel(level))
    


main()