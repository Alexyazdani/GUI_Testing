from PyQt6 import QtCore, QtGui, QtWidgets
from Gui_test import Ui_MainWindow

class Top_Level(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Top-Level GUI")
        self.icon_name_widget.setHidden(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Top_Level()
    MainWindow.show()
    sys.exit(app.exec())

