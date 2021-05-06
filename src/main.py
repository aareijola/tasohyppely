from GUI import GUI
import sys
from PyQt5.QtWidgets import QApplication

def main():
    global app
    app = QApplication(sys.argv)

    window = GUI()
    window.show()
    
    sys.exit(app.exec_())

main()