from PyQt5.QtWidgets import QApplication
from ui_login import LoginApp
import os

if __name__ == "__main__":
    app = QApplication([])
    win = LoginApp()
    win.show()
    app.exec_()