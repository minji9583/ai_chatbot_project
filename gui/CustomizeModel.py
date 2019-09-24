import sys
import os
import matplotlib.pyplot as plt
import pickle
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets, QtCore, QtGui
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MyApp(QWidget):
    css = """
        QWidget {
            color: #FFF;
            background: #FFF;
        }
        QWidget#windowTitle {
            color: #FFFFFF;
            background: #FFF;
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
        self.userTestres = [[], [], []];
        self.resize(600, 180)
        self.setFixedSize(600, 180)
        self.container = QtWidgets.QVBoxLayout(self)
        self.container.setContentsMargins(1, 1, 1, 1)

        self.setLayout(self.container)
        self.initUI()

    def initUI(self): 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #프레임을 없애고
        #self.setStyleSheet(self.css) # css를 적용함

        #타이틀 바 설정
        titlebar_widget =  MainTitleBar(self)
        #타이틀 바에 고유 아이디 등록(qss에 사용)
        titlebar_widget.setObjectName("windowTitle")

        self.container.addWidget(titlebar_widget)

        self.grid = QGridLayout()
        self.sFile = QLabel("선택한 파일이없습니다.")

        #학습 데이터 선택 라벨
        self.selectFileLb = QLabel('학습 데이터 선택 : ');

        #학습 데이터 경로
        self.sFile = QLabel("")

        # 파일 선택버튼
        self.selectFileBtn = QPushButton("파일 선택", self)
        self.selectFileBtn.clicked.connect(self.showFileDialog)
        self.selectFileBtn.setMaximumSize(100,30)
        self.selectFileBtn.setMinimumSize(100,30)

        # 빈공간 라벨
        self.blankHeight = QLabel("")
        self.blankHeight.setFixedHeight(0.05)
        
        # 학습 시작 버튼
        self.startBtn = QPushButton("학습 시작 >", self)
        self.startBtn.clicked.connect(self.start)
        self.startBtn.setMaximumSize(100,35)
        self.startBtn.setMinimumSize(100,35)

        #컨텐트 박스에 위젯들 붙이기
        self.contentBox = QGridLayout()
        self.contentBox.addWidget(self.selectFileLb,0,0)
        self.contentBox.addWidget(self.sFile,0,1)
        self.contentBox.addWidget(self.selectFileBtn,0,2)
  
        
        self.contentBox.addWidget(self.blankHeight,1,2)
        self.contentBox.addWidget(self.startBtn,2,2)

        #컨텐츠 박스를 step1 그룹박스에 붙이기
        self.step1 = QGroupBox("step1")
        self.step1.setLayout(self.contentBox)
        self.container.addWidget(self.step1)

    
        #타이틀바 위젯을 메인컨테이너에 붙이기
        self.container.addWidget(titlebar_widget)
        #step1을 메인컨테이너에 붙이기
        self.container.addWidget(self.step1)
             

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
        
        #여기에 프로그래스바가 생겨야하고... 끝나면 더 늘리기
        #프로그래스바는 나중에 했다치고, 프로그레스바가 끝나면 아래 버튼 이벤트가 실행되게
        self.step2 = QGroupBox("step2")
        self.container.addWidget(self.step2)
        self.grid = QGridLayout()
        self.step2.setLayout(self.grid)
        self.container.addStretch()
        self.tmpbtn = QPushButton("프로그레스바 컴플릿!", self);
        self.tmpbtn.clicked.connect(self.setFinalUI)
        self.grid.addWidget(self.tmpbtn, 0, 1)

    def setFinalUI(self):
        self.resize(600, 800)
        self.setFixedSize(600, 800)
        self.center()
        self.step2.deleteLater();

        #### 선언부 ####
        self.step3 = QGroupBox("step3 : 테스트 해보기")
        self.container.addWidget(self.step3)
        self.grid3 = QGridLayout()
        self.step3.setLayout(self.grid3)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.container.addWidget(self.canvas)
        self.canvas.draw();

        self.step4 = QGroupBox("step4 : 저장하기")
        self.container.addWidget(self.step4)
        self.grid4 = QGridLayout()
        self.step4.setLayout(self.grid4)


        #### 구현부 - step3 ####
        self.inputData = QLineEdit()
        self.inputData.setPlaceholderText("테스트할 문장을 입력하세요")
        self.inputData.setFocus();
        testBtn = QPushButton("test!");
        testBtn.clicked.connect(self.testData);
        self.outputData1 = QLabel("");
        self.outputData2 = QLabel("");
        self.outputData3 = QLabel("");

        self.grid3.addWidget(QLabel("입력값 : "),0,0)
        self.grid3.addWidget(self.inputData,0,1)
        self.grid3.addWidget(testBtn,0,2)
        self.grid3.addWidget(QLabel("출력값 : "), 1,0)
        self.grid3.addWidget(self.outputData1, 1,1,1,2)
        self.grid3.addWidget(self.outputData2, 2,1,2,2)
        self.grid3.addWidget(self.outputData3, 3,1,3,2);

        #### 구현부 - step4 ####
        selectbox = QGroupBox("학습 모델 선택")
        grid5 = QGridLayout()
        selectbox.setLayout(grid5)

        self.sPath = QLabel("")
        pathBtn = QPushButton("찾기")
        pathBtn.clicked.connect(self.showPathDialog)
        self.sFname = QLineEdit()
        saveBtn = QPushButton("저장")
        saveBtn.clicked.connect(self.saveCLF)

        self.radio1 = QRadioButton("A", self)
        self.radio2 = QRadioButton("B", self)
        self.radio3 = QRadioButton("C", self)
        self.radio1.setChecked(True)

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

    def testData(self):
        #사용자가 실험하고 싶은 문장
        testData = self.inputData.text();

        #TODO :: 원래라면, 학습모델에 데이터를 넣고 결과와 정확도를 뽑아내야함.
        #임의데이터
        self.userTestCnt = self.userTestCnt+1;
        self.userTestres[0].append((self.userTestCnt + 0) * self.userTestCnt)
        self.userTestres[1].append((self.userTestCnt + 1) * self.userTestCnt)
        self.userTestres[2].append((self.userTestCnt + 2) * self.userTestCnt)
        self.outputData1.setText("대략 바뀐 텍스트1" + testData)
        self.outputData2.setText("대략 바뀐 텍스트2" + testData)
        self.outputData3.setText("대략 바뀐 텍스트3" + testData)

        idx = np.arange(0, self.userTestCnt, 1)

        ax = self.fig.add_subplot(1,1,1)
        ax.plot(idx, self.userTestres[0])
        ax.plot(idx, self.userTestres[1])
        ax.plot(idx, self.userTestres[2])
        plt.xlabel('테스트 데이터')
        plt.ylabel('정확도')

        self.canvas.draw()

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        print("select : " + fname[0])
        self.sFile.setText(fname[0])

    def showPathDialog(self):
        pname = QFileDialog.getExistingDirectory()
        print("select : " + pname)
        self.sPath.setText(pname)

    def saveCLF(self):
        # 검증과정
        if self.sFname.text() == '':
            msg = QMessageBox()
            msg.setText("파일 이름을 입력하세요!")
            msg.exec()
            return;
        elif self.sPath.text()=='' :
            msg = QMessageBox()
            msg.setText("저장 경로를 선택하세요!")
            msg.exec()
            return;

        sAlgo = ""
        # 사용자가 선택한 저장할 학습 결과
        if self.radio1.isChecked() :
            res = 'A'
            sAlgo = "A알고리즘"
        elif self.radio2.isChecked():
            res = 'B'
            sAlgo = "B알고리즘"
        elif self.radio3.isChecked():
            res = 'C'
            sAlgo = "C알고리즘"

        # 사용자가 입력한 저장 파일 이름
        fname = self.sFname.text()

        path = self.sPath.text() + "//" + fname + ".clf"

        with open(path, 'wb') as f:
            pickle.dump(res, f);
            msg = QMessageBox()
            msg.setText(sAlgo + " : 저장되었습니다!")
            msg.exec()
        return

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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
    ex = MyApp()
    sys.exit(app.exec_())
