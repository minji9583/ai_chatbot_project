import sys
import matplotlib.pyplot as plt
import pickle
from PyQt5.QtWidgets import \
    QApplication, QWidget, QDesktopWidget, QGridLayout, QLabel, QPushButton, \
    QFileDialog, QLineEdit, QMessageBox, QBoxLayout, QGroupBox
from PyQt5 import QtWidgets, QtCore


class MyApp(QWidget):
    """메인 윈도우"""
    qss = """
        QWidget {
            color: #FFF;
            background: #4D342A;
        }
        QWidget#windowTitle {
            color: #FFFFFF;
            background: #FFFFFF;
        }
        QWidget#windowTitle QLabel {
            color: #000000;
            background: #FFFFFF;
        }
    """
    

    def __init__(self):
        super().__init__()
        self.userTestCnt = 0;
        self.userTestres = [];
        self.resize(600, 120)

        self.container = QGridLayout()
        self.setLayout(self.container)
        self.initUI()


    def initUI(self):
        self.step1 = QGroupBox("step1")
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #프레임을 없애고
        self.setStyleSheet(self.qss) # css를 적용함
        titlebar_widget = QtWidgets.QWidget()
        titlebar_widget.setObjectName("windowTitle")
        title_label = QtWidgets.QLabel("학습 장치")
        title_hbox = QtWidgets.QHBoxLayout(titlebar_widget)
        title_hbox.addWidget(title_label)
        self.container.addWidget(titlebar_widget,0,0)
        self.container.addWidget(self.step1,1,0)
        self.grid = QGridLayout()

        self.sFile = QLabel("선택한 파일이없습니다.")
        
        self.selectFileBtn = QPushButton("파일 선택", self)
        self.selectFileBtn.clicked.connect(self.showFileDialog)
        self.startBtn = QPushButton("학습 시작", self)
        self.startBtn.clicked.connect(self.start)
        self.selectFileLb = QLabel('학습 데이터 선택 : ');

        self.grid.addWidget(self.selectFileLb, 0, 0)
        self.grid.addWidget(self.sFile, 0, 1)
        self.grid.addWidget(self.selectFileBtn, 0,2)
        self.grid.addWidget(self.startBtn,1,1)
        
        self.step1.setLayout(self.grid)

        fname = QFileDialog.getOpenFileName(self)
        print("select : " + fname[0])
        self.sFile.setText(fname[0])

        self.center()
        self.show()

    def start(self):
        # 검증절차를 넣는다
        if self.sFile.text() == "" :
            msg = QMessageBox()
            msg.setText("학습데이터를 선택하세요!")
            msg.exec()
            return;

        # 다음단계로 넘어가면서
        # 새로운 도큐먼트들을 배치한다.
        self.setMoreUI()


    def setMoreUI(self):
        # 이전 내용을 모두 지우고 프로그래스바를 띄운다
        self.step1.deleteLater();


        #여기에 프로그래스바가 생겨야하고... 끝나면 더 늘리기
        #프로그래스바는 나중에 했다치고, 프로그레스바가 끝나면 아래 버튼 이벤트가 실행되게
        self.step2 = QGroupBox("step2")
        self.container.addWidget(self.step2)
        self.grid = QGridLayout()
        self.step2.setLayout(self.grid)

        self.tmpbtn = QPushButton("프로그레스바 컴플릿!", self);
        self.tmpbtn.clicked.connect(self.setFianlUI)
        self.grid.addWidget(self.tmpbtn, 1, 1)

    def setFianlUI(self):
        self.resize(600, 800)
        self.center()



######################################################
    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        print("select : " + fname[0])
        self.sFile.setText(fname[0])

    def showPathDialog(self):
        pname = QFileDialog.getExistingDirectory()
        print("select : " + pname)
        self.sPath.setText(pname)

    def saveCLF(self):
        # 학습 결과
        res = "this is result!"

        # 사용자가 입력한 저장 파일 이름
        fname = self.filename.text()

        path = self.sPath.text() + "//" + fname + ".clf"

        with open(path, 'wb') as f:
            pickle.dump(res, f);
            self.saveCompleteBox.exec()
        return

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
