from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QImage, QPixmap, QTextBlock
from rectbutton import RectButton
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QGraphicsRectItem, QLineEdit, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtCore import QRectF, Qt
from loader import listLevels
import psykoosi

class menu(QWidget):
    '''
    Menus for the game consist of four buttons and a text over the menu. They are all wrapped neatly into one widget with a QVBoxLayout.
    '''

    BUTTONWIDTH = 200
    BUTTONHEIGHT = 40
    MENUWIDTH = 260
    
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Box)
        self.frame.setLayout(QVBoxLayout())

        self.frame.setLineWidth(2)
        self.frame.setMaximumWidth(menu.MENUWIDTH)
        self.setLayout(QVBoxLayout())

        self.header = QLabel()
        self.layout().addWidget(self.header)
        self.layout().addWidget(self.frame, alignment = Qt.AlignCenter)
        self.buttons = []

        for i in range(4):
            button = RectButton()
            button.setMinimumSize(menu.BUTTONWIDTH, menu.BUTTONHEIGHT)
            button.setMaximumSize(menu.BUTTONWIDTH, menu.BUTTONHEIGHT)
            self.buttons.append(button)
            self.frame.layout().addWidget(button)
        
class mainMenu(menu):
    
    def __init__(self):
        super().__init__()
        self.header.setPixmap(QPixmap(psykoosi.MENU))
        self.buttons[0].setText("Opettele pelaamaan")
        self.buttons[1].setText("Lataa oma kenttä")
        self.buttons[2].setText("Kenttäeditori")
        self.buttons[3].setText("Poistu")
        self.layout().addWidget(QLabel("Valitse painamalla spacebar"), alignment = Qt.AlignCenter)

class gameMenu(menu):
    
    def __init__(self):
        super().__init__()
        self.header.setText("Tasohyppely tauolla :)")
        self.buttons[0].setText("Jatka pelaamista")
        self.buttons[1].setText("Takaisin päävalikkoon")
        self.buttons[2].setText("Poistu")
        self.buttons[3].hide()
        self.setMaximumWidth(240)
        
class alertPopup(QWidget):

    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Box)
        self.frame.setLayout(QVBoxLayout())
        self.frame.setLineWidth(2)
        self.frame.setMaximumWidth(500)
        self.buttons = []

        self.setLayout(QVBoxLayout())
        self.label = QLabel()
        self.layout().addWidget(self.frame, alignment = Qt.AlignCenter)
        self.frame.layout().addWidget(self.label)

class gameOverAlert(alertPopup):

    def __init__(self):
        super().__init__()
        
        self.label.setText("Oho, kuolit!")
        for i in range(2):
            button = RectButton()
            self.buttons.append(button)
            self.frame.layout().addWidget(button)
        self.buttons[0].setText("Yritä uudelleen")
        self.buttons[1].setText("Takaisin päävalikkoon")

class editorHelloPopup(alertPopup):

    def __init__(self):
        super().__init__()
        self.label.setText("Tervetuloa kenttäeditoriin!")
        self.setStyleSheet("Background-color:white;")
        for i in range(3):
            button = RectButton()
            self.buttons.append(button)
            self.frame.layout().addWidget(button)
        self.buttons[0].setText("Luo uusi kenttä")
        self.buttons[1].setText("Muokkaa vanhaa kenttää")
        self.buttons[2].setText("Takaisin päävalikkoon")

class levelSelect(alertPopup):
    
    def __init__(self):
        super().__init__()
        self.label.setText("Nykyiset tasot:")
        self.levels = listLevels()
        self.scrollArea = QScrollArea()
        self.frame.layout().addWidget(self.scrollArea, alignment = Qt.AlignCenter)
        self.frame.setFocusPolicy(Qt.NoFocus)
        self.scrollArea.setFixedWidth(230)
        self.scrollArea.setMaximumHeight(5 * menu.BUTTONHEIGHT)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFocusPolicy(Qt.NoFocus)
        newFrame = QFrame()
        newFrame.setLayout(QVBoxLayout())
        newFrame.setFrameStyle(QFrame.NoFrame)
        newFrame.setStyleSheet(
            'background-color:white; padding: 0px; border 0px;'
        )
        self.scrollArea.setWidget(newFrame)
        self.scrollArea.setWidgetResizable(True)
       
        for i in range(len(self.levels)):
            button = RectButton()
            self.buttons.append(button)
            self.buttons[i].setText(self.levels[i])
            newFrame.layout().addWidget(button)

class LevelCompleteAlert(alertPopup):

    def __init__(self):
        super().__init__()
        font = QtGui.QFont()
        font.setPointSize(12)
        #self.setStyleSheet("background-image:linear-gradient(to right, orange , yellow, green, cyan, blue, violet);")
        self.setStyleSheet("Background-color:pink;")

        self.label.setFont(font)
        self.label.setText("Onnittelut! Pääsit tason läpi!\nNyt voit valita toisen tason,\ntai tehdä kenttäeditorilla omiasi!")

        for i in range(2):
            button = RectButton()
            self.buttons.append(button)
            self.frame.layout().addWidget(button, alignment = Qt.AlignCenter)
        self.buttons[0].setText("Kokeile kenttäeditoria")
        self.buttons[1].setText("Takaisin päävalikkoon")

class EditorInfoBox(alertPopup):

    def __init__(self):
        super().__init__()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.setStyleSheet("Background-color:white;")
        btn = RectButton()
        btn.setText("OK!")
        self.buttons.append(btn)
        self.frame.layout().addWidget(btn, alignment = Qt.AlignCenter)


class EditorSideBar(menu):

    def __init__(self):
        super().__init__()
        for i in range(3):
            button = RectButton()
            button.setMinimumSize(menu.BUTTONWIDTH, menu.BUTTONHEIGHT)
            button.setMaximumSize(menu.BUTTONWIDTH, menu.BUTTONHEIGHT)
            self.buttons.append(button)
            self.frame.layout().addWidget(button)
        self.buttons[0].setText("[1] Palikka")
        self.buttons[1].setText("[2] Piikki")
        self.buttons[2].setText("[3] Kolikko")
        self.buttons[3].setText("[4] Mörkö")
        self.buttons[4].setText("[5] Maali")
        self.buttons[5].setText("[6] Pyyhekumi")
        self.buttons[6].setText("[ESC] Tallenna ja poistu")
        
class NameAlertBox(alertPopup):

    def __init__(self):
        super().__init__()
        self.setMaximumWidth(menu.MENUWIDTH)
        txt = QLabel("Anna kentällesi nimi:\n" + \
            "Huom: ääkköset ja erikois-\nmerkit poistetaan :)")
        font = QtGui.QFont()
        font.setPointSize(12)
        txt.setFont(font)

        self.setStyleSheet("Background-color:white;")
        self.frame.layout().addWidget(txt, alignment = Qt.AlignTop)
        self.line = QLineEdit("Mun kenttä")
        self.line.setStyleSheet("background-color:white;border:2px solid black")
        self.frame.layout().addWidget(self.line)
        self.line.setMaxLength(32)
        btn = RectButton()
        btn.setText("OK!")
        self.buttons.append(btn)
        self.frame.layout().addWidget(btn, alignment = Qt.AlignCenter)
        btn = RectButton()
        btn.setStyleSheet(("QPushButton {background-color : red;border : 3px solid black; font: bold}" + \
        "QPushButton:pressed {background-color : lightblue}" +  \
        "QPushButton:hover {background-color : lightblue}" + \
        "QPushButton:focus {outline : 3px solid black}"))
        btn.setText("Poistu tallentamatta")
        self.frame.layout().addWidget(btn, alignment = Qt.AlignCenter)
        self.buttons.append(btn)
        self.frame.layout().addWidget(btn, alignment = Qt.AlignCenter)