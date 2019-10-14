import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import pickle
import numpy as np

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ABChat(QWidget):

    def __init__(self):
        super().__init__()
        self.userTestCnt = 0;
        self.userTestres = [[], [], []];

        self.initUI()
        self.initMain()

    def initUI(self):
        # 타이틀바 설정
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.titlebar = MainTitleBar(self)
        self.titlebar.setObjectName("windowTitle")
        self.titlebar.backbtn.clicked.connect(self.initMain)

        self.vbox = QVBoxLayout()
        self.containerbox = QVBoxLayout()
        self.containerbox.addWidget(self.titlebar)
        self.containerbox.addLayout(self.vbox)
        self.setLayout(self.containerbox)

    def initMain(self):
        self.delPrevious()
        self.titlebar.backbtn.hide()

        pixmap = QPixmap("./img/ABChat.png")
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        learnBtn = QPushButton("학습하기")
        doTest = QPushButton("테스트하기")
        learnBtn.clicked.connect(self.initLearn)
        doTest.clicked.connect(self.initTest)

        self.vbox.addStretch(1)
        self.vbox.addWidget(logo)
        self.vbox.addStretch(2)
        self.vbox.addWidget(learnBtn)
        self.vbox.addWidget(doTest)
        self.vbox.addStretch(1)

        self.setWindowTitle('ABChat')
        self.resize(600, 400)
        self.setFixedSize(600,400)
        self.show()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def delPrevious(self):
        # 이전이 어떤 창이였든, 공통으로 쓰고있는 vbox의 아래에 있는 모든 위젯을 떼어냄
        for i in reversed(range(self.vbox.count())):
            # print(self.vbox.itemAt(i).widget())
            if self.vbox.itemAt(i).widget() != None:
                self.vbox.itemAt(i).widget().deleteLater()

    def initLearn(self):
        self.delPrevious()
        self.titlebar.backbtn.show()

        # 1. 선택
        h1box = QHBoxLayout()

        # 1-1. 알고리즘 선택
        grid1 = QGridLayout()
        group1 = QGroupBox("알고리즘 선택")
        group1.setLayout(grid1)
        h1box.addWidget(group1)

        radio1 = QRadioButton("로지스틱 알고리즘", self)
        radio2 = QRadioButton("네이브 알고리즘", self)
        radio3 = QRadioButton("또다른 어떠한 무언가의", self)
        radio1.setChecked(True)
        grid1.addWidget(radio1)
        grid1.addWidget(radio2)
        grid1.addWidget(radio3)

        # 1-2. 데이터 선택
        grid2 = QGridLayout()
        group2 = QGroupBox("")
        group2.setLayout(grid2)
        h1box.addWidget(group2)

        self.sData = QLabel("")
        self.fname = QLineEdit()
        dataSelectBtn = QPushButton("찾기")
        startBtn = QPushButton("학습 시작")

        grid2.addWidget(QLabel("선택 데이터 : "), 0, 0)
        grid2.addWidget(self.sData, 0, 1)
        grid2.addWidget(dataSelectBtn, 0, 2)
        grid2.addWidget(QLabel("저장이름 : "), 1, 0)
        grid2.addWidget(self.fname, 1, 1)
        grid2.addWidget(QLabel(".clf"), 1, 2)
        grid2.addWidget(startBtn, 2, 2)

        # 2. 진행
        g2box = QGridLayout()

        self.pbar = QProgressBar(self)
        openFolder = QPushButton("폴더열기")
        self.goTest = QPushButton("테스트하기")
        self.endBtn = QPushButton("종료")

        g2box.addWidget(self.pbar, 0, 0, 1, 3)
        g2box.addWidget(openFolder, 2, 0)
        g2box.addWidget(self.goTest, 2, 1)
        g2box.addWidget(self.endBtn, 2, 2)

        self.pbar.setValue(20)

        f1 = QFrame()
        f2 = QFrame()

        f1.setLayout(h1box)
        f2.setLayout(g2box)

        # 통합
        self.vbox.addStretch(2)
        #self.vbox.addLayout(h1box)
        self.vbox.addWidget(f1)
        self.vbox.addStretch(1)
        #self.vbox.addLayout(g2box)
        self.vbox.addWidget(f2)
        self.vbox.addStretch(2)

        self.setWindowTitle('학습하기')
        self.resize(600, 300)
        self.setFixedSize(600,300)
        self.show()
        self.center()

    def initTest(self):
        self.delPrevious()
        self.titlebar.backbtn.show()

        # 학습모델 조절
        box1 = QGroupBox("학습 모델 선택")
        self.test_grid1 = QGridLayout()
        box1.setLayout(self.test_grid1)

        self.sModel = QLabel("")
        modelSelectedBtn = QPushButton("찾기")
        startBtn = QPushButton("실험시작")

        self.test_grid1.addWidget(self.sModel, 0, 0, 1, 2)
        self.test_grid1.addWidget(modelSelectedBtn, 0, 2)
        self.test_grid1.addWidget(QLabel("저장된 데이터"), 1, 0)
        self.test_grid1.addWidget(startBtn, 5, 1)

        # 테스트 데이터 조절
        box2 = QGroupBox("테스트")
        test_vbox2 = QVBoxLayout()
        box2.setLayout(test_vbox2)

        self.inputData = QLineEdit()
        doTestBtn = QPushButton("테스트")
        self.output1 = QLabel()
        self.output2 = QLabel()
        self.output3 = QLabel()
        self.score1 = QLabel()
        self.score2 = QLabel()
        self.score3 = QLabel()

        inputgroup = QGridLayout()
        inputgroup.addWidget(QLabel("입력값"), 0, 0)
        inputgroup.addWidget(self.inputData, 0, 1)
        inputgroup.addWidget(doTestBtn, 0, 2)

        table = QGridLayout()
        table.addWidget(QLabel("출력값"), 0, 1)
        table.addWidget(QLabel("정확도"), 0, 2)
        table.addWidget(QLabel("로지스틱"), 1, 0)
        table.addWidget(QLabel("나이브"), 2, 0)
        table.addWidget(QLabel("어떤거"), 3, 0)
        table.addWidget(self.output1, 1, 1)
        table.addWidget(self.output2, 2, 1)
        table.addWidget(self.output3, 3, 1)
        table.addWidget(self.score1, 1, 2)
        table.addWidget(self.score2, 2, 2)
        table.addWidget(self.score3, 3, 2)

        test_vbox2.addLayout(inputgroup)
        test_vbox2.addLayout(table)

        # 그래프
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw();

        # 통합
        self.vbox.addStretch(2)
        self.vbox.addWidget(box1)
        self.vbox.addStretch(1)
        self.vbox.addWidget(box2)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.canvas)
        self.vbox.addStretch(2)

        self.setWindowTitle('학습모델 테스트')
        self.resize(600, 860)
        self.setFixedSize(600, 860)
        self.center()

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        print("select : " + fname[0])
        self.sData.setText(fname[0])

class MainTitleBar(QtWidgets.QWidget):
    """제목 표시줄 위젯"""
    qss = """
        QWidget {
            color: #FFFFFF;
            background: #4D342A;
            height: 32px;
        }
        QLabel {
            color: #FFFFFF;
            background: #4D342A;
            font-size: 16px;
            padding: 5px 5px;
        }
        QToolButton {
            background: #4D342A;
            border: none;
        }
        QToolButton:hover{
            background: #5E453B;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bar_height = 36
        self.parent = parent
        self.has_clicked = False
        self.is_maximized = False
        self.setStyleSheet(self.qss)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label = QtWidgets.QLabel("학습 장치")
        label.setFixedHeight(self.bar_height)
        btn_minimize = self.create_tool_btn('minimize_w.png')
        btn_minimize.clicked.connect(self.show_minimized)
        btn_close = self.create_tool_btn('close_w.png')
        btn_close.clicked.connect(self.close)
        self.backbtn = self.create_tool_btn('backbtn.png')
        #self.btn_back.clicked.connect(self.goback)

        layout.addWidget(self.backbtn)
        layout.addWidget(label)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)

    def create_tool_btn(self, icon_path):
        """제목표시줄 아이콘 생성"""
        icon = os.path.join(ROOT_PATH, 'img', icon_path)
        print(ROOT_PATH)
        btn = QtWidgets.QToolButton(self)
        btn.setIcon(QtGui.QIcon(icon))
        btn.setIconSize(QtCore.QSize(self.bar_height, self.bar_height))
        btn.setFixedSize(self.bar_height, self.bar_height)
        return btn

    def show_minimized(self):
        """버튼 명령: 최소화"""
        self.parent.showMinimized()

    def close(self):
        """버튼 명령: 닫기"""
        self.parent.close()


    def mousePressEvent(self, event):
        """오버로딩: 마우스 클릭 이벤트
        - 제목 표시줄 클릭시 이동 가능 플래그
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.parent.is_moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        """오버로딩: 마우스 이동 이벤트
        - 제목 표시줄 드래그시 창 이동
        """
        if self.parent.is_moving:
            self.parent.move(event.globalPos() - self.parent.offset)
    '''
    def mouseDoubleClickEvent(self, event):
        """오버로딩: 더블클릭 이벤트
        - 제목 표시줄 더블클릭시 최대화
        """
        if self.is_maximized:
            self.parent.showNormal()
            self.is_maximized = False
        else:
            self.parent.showMaximized()
            self.is_maximized = True

    '''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ABChat()
    sys.exit(app.exec_())


