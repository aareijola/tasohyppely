from leveleditor import LevelEditor
import menu
from game import platformerGame
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsView, QGridLayout, QLabel, QSpacerItem, QWidget, QLayout, QVBoxLayout, QHBoxLayout


class GUI(QtWidgets.QMainWindow):
    '''
    Main hub of all different widgets in the project. Also handles timers and menu elements.
    '''
    
    style = "QMainWindow {background-color : white;}"   #This is the stylesheet applied to the window

    def __init__(self):
        super().__init__()
        self.game = None
        self.selector = None
        self.view = None
        self.startMenu = menu.mainMenu()
        self.pauseMenu = menu.gameMenu()
        self.initStartMenu()
        self.initPauseMenu()
        self.initWindow()
        
    def initStartMenu(self):
        self.startMenu.buttons[3].clicked.connect(self.close)
        self.startMenu.buttons[0].clicked.connect(self.startTutorial)
        self.startMenu.buttons[1].clicked.connect(self.startOwnLevel)
        self.startMenu.buttons[2].clicked.connect(self.showLevelEditor)
    
    def initPauseMenu(self):
        self.pauseMenu.buttons[0].clicked.connect(self.unpauseGame)
        self.pauseMenu.buttons[1].clicked.connect(self.stopGame)
        self.pauseMenu.buttons[2].clicked.connect(self.close)
    

    def initView(self):
        if self.view:
            del(self.view)
        self.view = QGraphicsView(self.game.scene, self)
        self.view.setFocusPolicy(Qt.NoFocus)
        self.view.setLayout(QGridLayout())
        
        self.gametext = QLabel()
        self.gametext.setText("")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.gametext.setFont(font)
        
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.layout().addWidget(self.gametext, 0, 0, 1, 1, alignment = Qt.AlignTop)
        self.view.layout().addWidget(self.pauseMenu, 0, 1, 1, 1, alignment = Qt.AlignCenter)
        self.view.layout().addWidget(self.gameOverMenu, 0, 1, 1, 1, alignment = Qt.AlignCenter)

        self.view.layout().setColumnStretch(0, 1) 
        self.view.layout().setColumnStretch(1, 1)
        self.view.layout().setColumnStretch(2, 1)
   
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
    
    
    def initGameOver(self):
        self.gameOverMenu = menu.gameOverAlert()
        self.gameOverMenu.buttons[0].clicked.connect(self.resetGame)
        self.gameOverMenu.buttons[1].clicked.connect(self.stopGame)
        self.gameOverMenu.hide()
    
    
    def startGame(self, levelname):
        self.game = platformerGame(levelname)
        if self.game.unplayable:
            self.game = None
            self.showStartMenu()
        else:
            self.initGameOver()
            self.initView()
            self.initLevelCompleteWindow()
            self.centralWidget().layout().addWidget(self.view)
            self.hideStartMenu()
            self.view.show()
            self.timer = QTimer()
            self.timer.timeout.connect(self.updateGUI)
            self.timer.start(10)
    
    def startTutorial(self):
        self.startGame('Default')
    
    def selectorButtonClick(self, levelname):
        if self.selector:
            self.selector.hide()
            self.selector.setDisabled(True)
            self.selector.setFocusPolicy(Qt.NoFocus)

            self.startGame(levelname)
    
    def initGameLevelSelector(self):
        if self.selector:
            del(self.selector)
        self.selector = menu.levelSelect()
        self.centralWidget().layout().addWidget(self.selector)
        self.selector.show()
        for button in self.selector.buttons:
            button.clicked.connect(                                                         # we need the button text to choose level so we must use lambda.
                lambda button, text = button.text(): self.selectorButtonClick(text)         # https://stackoverflow.com/questions/45090982/passing-extra-arguments-through-connect
            )
        self.selector.buttons[0].setFocus()
    
    def startOwnLevel(self):
        self.hideStartMenu()
        self.initGameLevelSelector()

    def hideStartMenu(self):
        self.startMenu.hide()
        self.startMenu.setDisabled(True)
    
    def showStartMenu(self):
        self.startMenu.show()
        self.startMenu.setDisabled(False)
        self.startMenu.buttons[0].setFocus()

    def stopGame(self):
        self.unpauseGame()
        self.view.hide()
        self.timer = None
        self.game = None
        self.showStartMenu()

    def stopGameAndShowEditor(self):
        self.stopGame()
        self.showLevelEditor()

    def initLevelCompleteWindow(self):
        self.levelCompleteWindow = menu.LevelCompleteAlert()
        self.levelCompleteWindow.buttons[0].clicked.connect(self.stopGameAndShowEditor)
        self.levelCompleteWindow.buttons[1].clicked.connect(self.stopGame)
        self.view.layout().addWidget(self.levelCompleteWindow, 0, 1, 1, 1, alignment = Qt.AlignCenter)
        self.levelCompleteWindow.hide()    
    
    def showLevelCompleteWindow(self): 
        self.timer.stop()
        self.game = None
        self.timer = None
        self.levelCompleteWindow.show()
        self.levelCompleteWindow.buttons[0].setFocus()
    
    def showGameOver(self):
        self.gameOverMenu.show()
        self.timer.stop()
        self.gameOverMenu.setDisabled(False)
        self.gameOverMenu.buttons[0].setFocus()

    def hideGameOver(self):
        self.gameOverMenu.hide()
        self.gameOverMenu.setDisabled(True)
    
    def resetGame(self):
        currentlevel = self.game.level.name
        self.stopGame()
        self.hideGameOver()
        self.startGame(currentlevel)

    def pauseGame(self):
        """
        When the game is paused the pause menu is shown and all gameplay is freezed.
        """
        self.game.pause()
        self.timer.stop()
 
        self.pauseMenu.setDisabled(False)
        self.pauseMenu.show()
        self.pauseMenu.buttons[0].setFocus()

    def unpauseGame(self):
        """
        Unpausing the game hides the pause menu and disables all input for it. Gameplay resumes after.
        """
        if self.game:
            self.game.unpause()
        self.pauseMenu.hide()
        self.pauseMenu.setDisabled(True)
        self.view.show()
        if self.timer:
            self.timer.start(10)

    def updateGUI(self):
        if not self.game.gameover:
            victory = self.game.updateGame()
            self.gametext.setText(self.game.gameText())
            self.view.centerOn(self.game.player)
            if victory:
                self.showLevelCompleteWindow()
        else:
            self.showGameOver()

    def hideEditorHello(self):
        self.view.layout().removeWidget(self.editorpopup)
        self.editorpopup.hide()
        self.editorpopup.setDisabled(True)
            
    def startOwnEdit(self,text):
        self.selector.hide()
        self.selector.setDisabled(True)
        self.selector.setFocusPolicy(Qt.NoFocus)
        self.view.setLevel(text)
        
        self.view.exitbutton.clicked.connect(self.closeLevelEditor)
        self.view.startEdit()

        

    def initEditorLevelSelector(self):
        if self.selector:
            del(self.selector)
        self.selector = menu.levelSelect()
        self.view.layout().addWidget(self.selector,1,1,1,1, alignment = Qt.AlignCenter)
        self.selector.show()
        self.hideEditorHello()
        for button in self.selector.buttons:
            button.clicked.connect(                                                         
                lambda button, text = button.text(): self.startOwnEdit(text)         
            )
        self.selector.buttons[0].setFocus()
        
    def editNew(self):
        self.view.setLevel('new')
        self.hideEditorHello()
        
        self.view.exitbutton.clicked.connect(self.closeLevelEditor)
        self.view.startEdit()   
        

    def showEditorHello(self):
        self.editorpopup = menu.editorHelloPopup()
        self.view.layout().addWidget(self.editorpopup,1,1,1,1, alignment = Qt.AlignCenter)
        self.editorpopup.buttons[0].clicked.connect(self.editNew)
        self.editorpopup.buttons[1].clicked.connect(self.initEditorLevelSelector)
        self.editorpopup.buttons[2].clicked.connect(self.closeLevelEditor)
    
    def showLevelEditor(self):
        self.view = LevelEditor(self)
        self.showEditorHello()
        self.startMenu.hide()
        self.startMenu.setDisabled(True)
        self.centralWidget().layout().addWidget(self.view)
        self.view.show()
        self.editorpopup.buttons[0].setFocus()

    def closeLevelEditor(self):
        self.centralWidget().layout().removeWidget(self.view)
        self.view = None
        self.showStartMenu()


    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape and self.game:
            if self.game.isPaused():
                self.unpauseGame()
            elif not self.game.isPaused() and not self.game.gameover:
                self.pauseGame()
        if self.game:
            self.game.keyPressEvent(a0)
    
    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.game:
            self.game.keyReleaseEvent(a0)