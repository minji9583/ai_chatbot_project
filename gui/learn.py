import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class LearnModel(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('LearnMdoel')
        self.resize(100, 100)
        self.show()
        self.center()

    def initUI(self):

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(QLabel("this is learn model"))
        vbox.addStretch(1)

        self.setLayout(vbox)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = LearnModel()
#     sys.exit(app.exec_())