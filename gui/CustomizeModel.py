import sys
import matplotlib.pyplot as plt
import pickle
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore


class MyApp(QWidget):
    css = """
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
        QGroupBox  {
            border: 1px solid gray;
            margin: 10px;
            font-size: 14px;
            border-radius: 15px;
        }
        
    """
    

    def __init__(self):
        super().__init__()
        self.userTestCnt = 0;
        self.userTestres = [];
        self.resize(600, 120)
        
        self.container = QtWidgets.QVBoxLayout(self)
        self.container.setContentsMargins(1, 1, 1, 1)

        self.setLayout(self.container)
        self.initUI()


    def initUI(self): 
        self.step1 = QGroupBox("step1")
            
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #프레임을 없애고
        self.setStyleSheet(self.css) # css를 적용함

        titlebar_widget = QtWidgets.QWidget()
        titlebar_widget.setObjectName("windowTitle")
        title_label = QtWidgets.QLabel("학습 장치")
        title_hbox = QtWidgets.QHBoxLayout(titlebar_widget)
        title_hbox.addWidget(title_label)
        
        self.container.addWidget(titlebar_widget)
        self.container.addWidget(self.step1)
        
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

        # 다음단계로 넘어가면서 새로운 도큐먼트들을 배치한다.
        self.setMoreUI()

    def setMoreUI(self):
        # 이전 내용을 모두 지우고 프로그래스바를 띄운다
        self.step1.deleteLater();


        # 여기에 프로그래스바가 생겨야하고... 끝나면 더 늘리기
        # 프로그래스바는 나중에 했다치고, 프로그레스바가 끝나면 아래 버튼 이벤트가 실행되게
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
        self.step2.deleteLater();

        self.step3 = QGroupBox("step3 : 테스트 해보기")
        self.container.addWidget(self.step3)
        self.grid3 = QGridLayout()
        self.step3.setLayout(self.grid3)

        self.step4 = QGroupBox("step4 : 저장하기")
        self.container.addWidget(self.step4)
        self.grid4 = QGridLayout()
        self.step4.setLayout(self.grid4)

        inputData = QLineEdit()
        inputData.setPlaceholderText("테스트할 문장을 입력하세요")
        inputData.setFocus();
        testBtn = QPushButton("test!");
        #testBtn.clicked.connect(None);
        self.outputData1 = QLabel("111111111111111");
        self.outputData2 = QLabel("222222222222222");
        self.outputData3 = QLabel("33333333333333");

        self.grid3.addWidget(QLabel("입력값 : "),0,0)
        self.grid3.addWidget(inputData,0,1)
        self.grid3.addWidget(testBtn,0,2)
        self.grid3.addWidget(QLabel("출력값 : "), 1,0)
        self.grid3.addWidget(self.outputData1, 1,1,1,2)
        self.grid3.addWidget(self.outputData2, 2,1,2,2)
        self.grid3.addWidget(self.outputData3, 3,1,3,2);

        selectbox = QGroupBox("학습 모델 선택")
        grid5 = QGridLayout()
        selectbox.setLayout(grid5)

        self.sPath = QLabel("")
        pathBtn = QPushButton("찾기")
        self.sFname = QLineEdit()
        saveBtn = QPushButton("저장")

        self.radio1 = QRadioButton("A", self)
        self.radio2 = QRadioButton("B", self)
        self.radio3 = QRadioButton("C", self)

        grid5.addWidget(self.radio1, 0, 0)
        grid5.addWidget(self.radio2, 0, 1)
        grid5.addWidget(self.radio3, 0, 2)

        self.grid4.addWidget(selectbox, 0,0)
        self.grid4.addWidget(QLabel("경로 선택 : "), 1,0)
        self.grid4.addWidget(self.sPath,1,1)
        self.grid4.addWidget(pathBtn,1,2)
        self.grid4.addWidget(QLabel("파일 이름 : "), 2,0)
        self.grid4.addWidget(self.sFname,2,1)
        self.grid4.addWidget(QLabel(".clf"))
        self.grid4.addWidget(saveBtn,3,1)


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
