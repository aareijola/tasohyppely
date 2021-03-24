from GUI import GUI
from rectbutton import RectButton
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


def main():
    global app
    app = QApplication(sys.argv)

    window = GUI()
    
    sys.exit(app.exec_())

main()