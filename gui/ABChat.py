import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

import learn

tag = 0;


class ABChat(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('ABChat')
        self.resize(600, 400)
        self.show()
        self.center()

    def initUI(self):
        pixmap = QPixmap("./img/ABChat.png")
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        learnBtn = QPushButton("학습하기")
        doTest = QPushButton("테스트하기")
        openServer = QPushButton("서버열기")
        learnBtn.clicked.connect(self.createLearn)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(logo)
        vbox.addStretch(2)
        vbox.addWidget(learnBtn)
        vbox.addWidget(doTest)
        vbox.addWidget(openServer)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createLearn(self):
        # QCoreApplication.instance().quit
        str = ["C:/Users/multicampus/Desktop/Project119/ai-sub3/gui/learn.py"]
        ll = QApplication(str)
        lmodel = learn.LearnModel()
        #lmodel.exec_()
        ll.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ABChat()
    sys.exit(app.exec_())


