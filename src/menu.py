from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QTextBlock
from rectbutton import RectButton
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGridLayout, QLabel, QGraphicsRectItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QRectF, Qt

class menu(QWidget):
    '''
    Menus for the game consist of four buttons and a text over the menu. They are all wrapped neatly into one widget with a QVBoxLayout.
    '''

    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Box)
        self.frame.setLayout(QVBoxLayout())

        self.frame.setLineWidth(2)
        self.frame.setMaximumWidth(220)
        self.setLayout(QVBoxLayout())

        self.header = QLabel()
        self.layout().addWidget(self.header)
        self.layout().addWidget(self.frame, alignment = Qt.AlignCenter)
        self.buttons = []

        for i in range(4):
            button = RectButton()
            button.setMinimumSize(200, 40)
            button.setMaximumSize(200, 40)
            self.buttons.append(button)
            self.frame.layout().addWidget(button)

        
        
        
class mainMenu(menu):
    
    def __init__(self):
        super().__init__()
        self.header.setPixmap(QPixmap("data/title.png"))
        self.buttons[0].setText("Aloita peli")
        self.buttons[1].setText("Kenttäeditori")
        self.buttons[2].setText("Asetukset")
        self.buttons[3].setText("Poistu")
        self.layout().addWidget(QLabel("Valitse painamalla spacebar"), alignment = Qt.AlignCenter)

class gameMenu(menu):
    
    def __init__(self):
        super().__init__()
        self.header.setText("Tasohyppely tauolla :)")
        self.buttons[0].setText("Jatka pelaamista")
        self.buttons[1].setText("Takaisin päävalikkoon")
        self.buttons[2].setText("Asetukset")
        self.buttons[3].setText("Poistu")
        self.setMaximumWidth(240)
        
