import menu
from game import Game
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsView, QWidget, QLayout, QVBoxLayout, QHBoxLayout


class GUI(QtWidgets.QMainWindow):
    '''
    Main component of all different widgets in the project. Also handles timers and menu elements.
    '''
    
    style = "background-color : white"   #This is the stylesheet applied to the window

    def __init__(self):
        super().__init__()
        self.game = None
        self.startMenu = menu.mainMenu()
        self.pauseMenu = menu.gameMenu()
        self.initStartMenu()
        self.initPauseMenu()
        self.initWindow()
        
    def initStartMenu(self):
        self.startMenu.buttons[3].clicked.connect(self.close)
        self.startMenu.buttons[0].clicked.connect(self.startGame)
    
    def initPauseMenu(self):
        self.pauseMenu.buttons[0].clicked.connect(self.unpauseGame)
        self.pauseMenu.buttons[1].clicked.connect(self.stopGame)
        self.pauseMenu.buttons[3].clicked.connect(self.close)
    
    def initView(self):
        self.view = QGraphicsView(self.game.scene, self)
        self.view.setLayout(QVBoxLayout())
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.layout().addWidget(self.pauseMenu, alignment = Qt.AlignCenter)
        self.pauseMenu.hide()
        self.view.hide()
    
    
    def initWindow(self):
        self.setCentralWidget(QWidget())
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle("Tasohyppelypeli")

        self.centralWidget().setLayout(QVBoxLayout())
        
        self.centralWidget().layout().setAlignment(Qt.AlignCenter)
        self.centralWidget().layout().addWidget(self.startMenu)

        self.setStyleSheet(GUI.style)
        
        self.show()    
    
    
    
    
    def startGame(self):
        self.game = Game()
        self.initView()
        self.centralWidget().layout().addWidget(self.view)

        self.startMenu.hide()
        self.view.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGUI)
        self.timer.start(10)
    
    def stopGame(self):
        self.unpauseGame()
        self.view.hide()
        self.timer = None
        self.game = None #################### Tähän jotain millä resetataan peli?
        self.startMenu.show()


    def pauseGame(self):
        self.game.pause()
        self.timer.stop()
        #self.view.hide()
        self.pauseMenu.show()

    def unpauseGame(self):
        self.game.unpause()
        self.pauseMenu.hide()
        self.view.show()
        self.timer.start(10)
    
    def updateGUI(self):
        self.game.updateGame()
        self.view.centerOn(self.game.player)


    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape and self.game:
            if self.game.isPaused():
                self.unpauseGame()
            elif not self.game.isPaused():
                self.pauseGame()
        if a0.key() not in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            return super().keyPressEvent(a0)