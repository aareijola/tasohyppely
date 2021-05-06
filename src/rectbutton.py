from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton, QAbstractButton

class RectButton(QPushButton):
    '''
    This class exists to help experiment with different looks for RectButton elements.
    '''
    BUTTONWIDTH = 200
    BUTTONHEIGHT = 40
    
    style = "QPushButton {background-color : white;border : 3px solid black; font: bold}" + \
        "QPushButton:pressed {background-color : lightblue}" +  \
        "QPushButton:hover {background-color : lightblue}" + \
        "QPushButton:focus {outline : 3px solid black}"
        
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet(RectButton.style)
        self.setMinimumSize(RectButton.BUTTONWIDTH, RectButton.BUTTONHEIGHT)
        self.setMaximumSize(RectButton.BUTTONWIDTH, RectButton.BUTTONHEIGHT)