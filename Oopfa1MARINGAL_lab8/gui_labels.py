import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QIcon


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt Line Edit"
        self.x = 200  # Left position
        self.y = 200  # Top position
        self.width = 300
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)

        # Ensure the icon file exists in the correct path
        self.setWindowIcon(QIcon('pencil_icon_264163.ico'))

        # Creating Labels
        self.textboxlbl = QLabel("Hello World!", self)
        self.textboxlbl.move(100, 100)

        self.textboxlbl2 = QLabel("This program is written in PyCharm", self)
        self.textboxlbl2.move(50, 130)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
