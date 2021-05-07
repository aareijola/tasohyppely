from os import name
from PyQt5.QtGui import QFont
from characters import *
from typing import Text
from PyQt5.QtCore import QTimer, Qt
from menu import *
from loader import loadLevel, saveLevel
from gamelevel import GameLevel
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QLayout


class LevelEditor(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent, alignment = Qt.AlignCenter)
        self.setLayout(QGridLayout())
        self.layout().setColumnStretch(0, 1) 
        self.layout().setColumnStretch(1, 1)
        self.layout().setColumnStretch(2, 1)

        self.layout().setRowStretch(0, 1) 
        self.layout().setRowStretch(1, 1)
        self.layout().setRowStretch(2, 1)

        self.setFocusPolicy(Qt.NoFocus)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.blockBrush = QBrush(QColor(128, 64, 0))
        self.blockPen = QPen()
        self.blockPen.setWidth(3)
        self.nameAlertBox = None
        self.nogoal = None

        self.camera = Camera()
        self.exitbutton = RectButton()
        self.selection = 'Block'
        self.lastselection = None
        self.last = []
        self.firstClick = None
        self.level = None
        self.editorTimer = QTimer()
        self.editorTimer.timeout.connect(self.focusCamera)
        sz = Character.CHARSIZE

    def setLevel(self, level):
        if level.lower() == 'new':
            self.level = GameLevel()
        else:
            self.level = loadLevel(level)
            if not self.level:
                self.level = GameLevel()
        self.level.setSpawn(QPointF(0,0))
        self.scene = self.level.generateScene()
        self.setScene(self.scene)
        self.scene.addItem(self.camera)


    def addSelectedItem(self, scenepos):

        item = None
        if self.selection is None:
            pass
        else:
            sz = Character.CHARSIZE
            # Here, the amount the items need to be moved in the scene depends on their Brush, because a wrong amount will mess up the looks.
            if self.selection == 'Block':
                item = QGraphicsRectItem(-sz / 2,-sz / 2, sz, sz)
                item.moveBy(scenepos.x(), scenepos.y())
            elif self.selection == 'Spike':
                item = Spike(scenepos.x(), scenepos.y())
                item.moveBy(scenepos.x(), scenepos.y())
            elif self.selection == 'Coin':
                item = Coin(scenepos.x() - sz/ 2, scenepos.y()- sz / 2)
                item.moveBy(scenepos.x() - sz/2, scenepos.y() - sz/ 2)

            elif self.selection == 'Finish' and self.level.finish is None:
                ## Tässä vois näyttää warningin jos maali on jo!
                item = Goal()
                item.moveBy(scenepos.x() - sz/2, scenepos.y() - sz/ 2)
                self.level.setFinish(scenepos)

            if item:
                self.addToLevel(item)
    
    def addToLevel(self, item):
        self.scene.addItem(item)
        if type(item) in [QGraphicsRectItem, Spike]:
            if type(item) == QGraphicsRectItem:
                if len(item.collidingItems()) > 0:
                    self.scene.removeItem(item)
                    del(item)
                    return      
            else:
                if self.level.player in item.collidingItems():
                    self.scene.removeItem(item)
                    del(item)
                    return
            self.level.objects.append(item)
        elif type(item) == Goal:
            if self.level.player in item.collidingItems():
                self.scene.removeItem(item)
                self.level.finish = None
                del(item)
                return
        
        elif type(item) == Coin:
            self.level.coins.append(item)
        elif type(item) == Enemy:
            if len(item.collidingItems()) > 0:
                self.scene.removeItem(item)
                del(item)
                return
            else:   
                self.level.characters.append(item)
        
        self.last.append(item)
    
    def focusCamera(self):
        self.camera.update()
        self.centerOn(self.camera)
        self.camera.setFocus()
        self.updateSideText()
        if not self.selection == self.lastselection:
            self.firstClick = None

        
    def updateSideText(self):
        item = 'Ei mitään'
        if self.selection == 'Block':
            item = 'Palikka'
        if self.selection == 'Spike':
            item = 'Piikki'
        if self.selection == 'Coin':
            item = 'Kolikko'
        if self.selection == 'Finish':
            item = 'Maali'
        if self.selection == 'Enemy':
            item = 'Mörkö'
        if self.selection == 'Delete':
            item = 'Pyyhekumi'

        if self.level.name:
            txt = "Tason nimi:{}\n".format(self.level.name) + \
            "Valittu esine:{}\n".format(item)
        else:
            txt = "Valittu esine:{}\n".format(item)
        
        
        self.sideText.setText(txt)
    
    
    def startEdit(self):
        """
        First thing called on editor startup. Shows an info box to the user.
        """
        txt = "Lisäile pelielementtejä ruudulle hiirellä napsauttamalla. :)\n" \
            + "Palikan voit lisätä napsauttamalla vastakkaisia kulmia.\n" \
            + "Pahiksenkin lisääminen tapahtuu klikkaamalla ensin liikeradan\n" \
            + "alkupistettä, ja sitten päätepistettä.\nHuomaathan, että möröt eivät osaa läpäistä kolikoita!\n\n" \
            + "Editorissa voit liikuttaa kameraneliötä WASD-näppäimillä. \n"\
            + "Z-näppäin poistaa edellisen lisätyn esineen.\n" \
            + "Lisäksi voit zoomata hiiren rullalla.\n" \
            + "Vinkki: älä rakenna liian alas, \n" \
            + "sillä pelissä maailma loppuu, kun y = 1000!"
        box = EditorInfoBox()
        box.label.setText(txt)
        self.layout().addWidget(box, 1, 1, 1, 1, alignment = Qt.AlignCenter)
        box.buttons[0].clicked.connect(box.hide)
        box.buttons[0].setFocus()
        self.editorTimer.start(10)
        self.sideText = QLabel()
        font = QFont()
        font.setPointSize(15)
        self.sideText.setFont(font)
        self.layout().addWidget(self.sideText, 0, 0, 1, 1, alignment = Qt.AlignTop)


        self.sideText.setText("KAMOON")

        sidebox = EditorSideBar()
        sidebox.buttons[0].clicked.connect(self.selectBlock)
        sidebox.buttons[1].clicked.connect(self.selectSpike)
        sidebox.buttons[2].clicked.connect(self.selectCoin)
        sidebox.buttons[3].clicked.connect(self.selectEnemy)
        sidebox.buttons[4].clicked.connect(self.selectGoal)
        sidebox.buttons[5].clicked.connect(self.selectDelete)
        sidebox.buttons[6].clicked.connect(self.saveAndQuit)
        sidebox.setDisabled(True)

        box.buttons[0].clicked.connect(lambda: sidebox.setDisabled(False))

        self.layout().addWidget(sidebox, 1, 0, 1, 1, alignment = Qt.AlignLeft)
        #self.setMouseTracking(True)

    def deleteItemAt(self, coords):
        item = self.itemAt(self.mapFromScene(coords.x(), coords.y()))
        if item:
            if type(item) not in [Camera, Player]:
                self.removeFromLevel(item)

    def selectBlock(self):
        self.lastselection = self.selection
        self.selection = 'Block'

    def selectSpike(self):
        self.lastselection = self.selection
        self.selection = 'Spike'

    def selectCoin(self):
        self.lastselection = self.selection
        self.selection = 'Coin'
    
    def selectEnemy(self):
        self.lastselection = self.selection
        self.selection = 'Enemy'

    def selectGoal(self):
        self.lastselection = self.selection
        self.selection = 'Finish'

    def selectDelete(self):
        self.lastselection = self.selection
        self.selection = 'Delete'
    
    def deleteLast(self):
        """
        Removes the last item added from the scene.
        """
        if len(self.last) > 0:
            item = self.last.pop()
            self.removeFromLevel(item)
            
    def removeFromLevel(self, item):
        self.scene.removeItem(item)
        if type(item) in [QGraphicsRectItem, Spike]:
            self.level.objects.remove(item)
        elif type(item) == Coin:
            self.level.coins.remove(item)
        elif type(item) == Goal:
            self.level.finish = None
        elif type(item) == Enemy:
            self.level.characters.remove(item)

        if item in self.last:
            self.last.remove(item)
        item.hide()
        del(item)

    def noFinishAlert(self):
        if self.nogoal:
            self.layout().removeWidget(self.nogoal)
            del(self.nogoal)
            self.nogoal = None
        txt = "Et voi tallentaa kenttää jossa ei ole maalia!\n" + \
            "Valitse [5] Maali, ja lisää se kenttään jatkaaksesi! :)"
        self.nogoal = EditorInfoBox()
        self.nogoal.label.setText(txt)
        btn = RectButton()
        btn.setText("Poistu tallentamatta")
        btn.setStyleSheet("QPushButton {background-color : red;border : 3px solid black; font: bold}" + \
        "QPushButton:pressed {background-color : lightblue}" +  \
        "QPushButton:hover {background-color : lightblue}" + \
        "QPushButton:focus {outline : 3px solid black}")
        self.nogoal.frame.layout().addWidget(btn, alignment = Qt.AlignCenter)
        self.nogoal.buttons.append(btn)
        self.layout().addWidget(self.nogoal, 1, 1, 1, 1, alignment = Qt.AlignCenter)
        self.nogoal.buttons[0].clicked.connect(self.nogoal.hide)
        self.nogoal.buttons[1].clicked.connect(self.exitbutton.click)
    
    def setLevelName(self):
        name = self.nameAlertBox.line.text()
        name = "".join(l for l in name if l.isalnum() and l not in 'öÖäÄ')
        self.level.setName(name)
        saveLevel(self.level)
        self.exitbutton.click()

    def saveAndQuit(self):
        if self.level:
            if self.level.isPlayable():
                if self.nameAlertBox:
                    self.layout().removeWidget(self.nameAlertBox)
                    del(self.nameAlertBox)
                    self.nameAlertBox = None
                self.nameAlertBox = NameAlertBox()
                if self.level.name != 'Default':
                    self.nameAlertBox.line.setText(self.level.name) 
                self.layout().addWidget(self.nameAlertBox, 1,1,1,1, alignment = Qt.AlignCenter)
                self.nameAlertBox.buttons[0].clicked.connect(self.setLevelName)
                self.nameAlertBox.buttons[1].clicked.connect(self.exitbutton.click)

            else:
                self.noFinishAlert()

    def mousePressEvent(self, a0) -> None:
        # Blocks are added separately because they need 2 clicks
        scenecoords = self.mapToScene(self.mapFromGlobal(a0.globalPos()))
        if self.selection == 'Delete':
            self.deleteItemAt(scenecoords)
        
        if self.selection not in ['Block', 'Enemy']:
            self.addSelectedItem(scenecoords)
            self.firstClick = None
        elif self.selection == 'Block':
            if self.firstClick:
                secondClick = scenecoords
                w = abs(self.firstClick.x() - secondClick.x()) # Even though there is a QRectF constructor for QGraphicsRectItem, I noticed that using it with just
                h = abs(self.firstClick.y() - secondClick.y()) # the two click locations sometimes results in negative width/height values which
                topleft  = QPointF(                            # creates blocks with a hitbox different than its graphic. This way the block is always
                    min(                                       # spawned from the topleft corner with correct positive width/height values.
                        self.firstClick.x(),
                        secondClick.x()
                    ),
                    min(
                        self.firstClick.y(),
                        secondClick.y()
                    )
                )    
                item = QGraphicsRectItem(topleft.x(), topleft.y(), w, h)
                item.setBrush(self.blockBrush)
                item.setPen(self.blockPen)
                self.addToLevel(item)
                self.firstClick = None
            else:
                self.lastselection = self.selection
                self.firstClick = scenecoords
        # Also enemies are spawned here for the same reason as blocks
        elif self.selection == 'Enemy':
                if self.firstClick:
                    sz = Character.CHARSIZE
                    item = Enemy()
                    real_X = self.firstClick.x() - sz/2
                    real_Y = self.firstClick.y() - sz/ 2
                    second_X = scenecoords.x() - sz/2
                    second_Y = scenecoords.y() -sz/2
                    item.moveBy(real_X, real_Y)
                    item.setTrajectory([QPointF(real_X, real_Y), QPointF(scenecoords.x(), self.firstClick.y())])
                    self.addToLevel(item)
                    self.firstClick = None
                else:
                    self.lastselection = self.selection
                    self.firstClick = scenecoords

    # Keybindings:
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape and self.level:
            self.saveAndQuit()
        if a0.key() == Qt.Key_Z:
            self.deleteLast()
        if a0.key() == Qt.Key_2:
            self.selectSpike()
        if a0.key() == Qt.Key_1:
            self.selectBlock()
        if a0.key() == Qt.Key_4:
            self.selectEnemy()
        if a0.key() == Qt.Key_5:
            self.selectGoal()
        if a0.key() == Qt.Key_3:
            self.selectCoin()
        if a0.key() == Qt.Key_6:
            self.selectDelete()

        # Camera movement stuff
        if a0.key() in [Qt.Key_A, Qt.Key_Left]:
            self.camera.movingLeft = True
        if a0.key() in [Qt.Key_D, Qt.Key_Right]:
            self.camera.movingRight = True
        if a0.key() in [Qt.Key_W, Qt.Key_Up]:
            self.camera.movingUp = True
        if a0.key() in [Qt.Key_S, Qt.Key_Down]:
            self.camera.movingDown = True
    
    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() in [Qt.Key_A, Qt.Key_Left]:
            self.camera.movingLeft = False
        if a0.key() in [Qt.Key_D, Qt.Key_Right]:
            self.camera.movingRight = False
        if a0.key() in [Qt.Key_W, Qt.Key_Up]:
            self.camera.movingUp = False
        if a0.key() in [Qt.Key_S, Qt.Key_Down]:
            self.camera.movingDown = False
    
    
    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        # This handles zooming
        angle = event.angleDelta().y()
        if angle > 0:
            self.scale(1.2, 1.2)
        else:
            self.scale(1/1.2, 1/1.2)