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

import numpy as np
from konlpy.tag import Okt
from scipy.sparse import lil_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

import time
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
        self.resize(600, 280)
        self.setFixedSize(600, 280)
        
        self.container = QtWidgets.QVBoxLayout(self)
        self.container.setContentsMargins(1, 1, 1, 1)
        self.pbarValue = 0
        
        self.setLayout(self.container)
        self.initUI()
        self.okt = Okt()
        self.flag = False
        """
        Req 1-1-1. 데이터 읽기
        read_data(): 데이터를 읽어서 저장하는 함수
        """


    def read_data(self,filename):
        print(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            datas = [line.split('\t') for line in f.read().splitlines()]
            datas = datas[1:]
        return datas
        """
        Req 1-1-2. 토큰화 함수
        tokenize(): 텍스트 데이터를 받아 KoNLPy의 okt 형태소 분석기로 토크나이징
        """
    
    
    def tokenize(self,doc):
        print("토크나이즈1")
        tt = self.okt.pos(doc, norm=True, stem=True)
        print("토크나이즈2")
        return ['/'.join(t) for t in tt]

    def preprocess(self,slack_str):
        print("프리프로세스 시작이에요")
        X_test2 = lil_matrix((1, len(self.word_indices) + 1), dtype=int)
        test_str = slack_str
        okt = Okt()
        tokenize = okt.pos(test_str, norm=True, stem=True)
        test_tokens = ['/'.join(t) for t in tokenize]
        none_cnt = 0
        print("포문시작")
        for token in test_tokens:
            indices = self.word_indices.get(token)
            if indices:
                X_test2[0, indices] = 1
                
        print("포문끝났다")
        
        return X_test2[0]

    def classify1(self,X_test):
        result1 = self.clf.predict(X_test)
        if result1 == 1:
            return "긍정"
        else:
            return "부정"

    def classify2(self,X_test):
      
        result2 = self.clf2.predict(X_test)
        if result2 == 1:
            return "긍정"
        else:
            return "부정"

        
    def classify3(self,X_test):
        result3 = self.knn.predict(X_test)
        if result3 == 1:
            return "긍정"
        else:
            return "부정"
        

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
        self.selectFileLb = QLabel('Selected File : ');

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
        self.gkrBtn = QPushButton("학습하기", self)
        self.gkrBtn.clicked.connect(self.gkrtmq)

        #컨텐트 박스에 위젯들 붙이기
        self.contentBox = QGridLayout()
        self.contentBox.addWidget(self.selectFileLb,0,0)
        self.contentBox.addWidget(self.sFile,0,1)
        self.contentBox.addWidget(self.selectFileBtn,0,2)
        self.contentBox.addWidget(self.blankHeight,1,2)
        self.contentBox.addWidget(self.gkrBtn,2,2)

        #컨텐츠 박스를 step1 그룹박스에 붙이기
        self.step1 = QGroupBox("step1 : 학습시킬 데이터 파일을 선택합니다.")
        self.step1.setLayout(self.contentBox)
        self.container.addWidget(self.step1)

        #타이틀바 위젯을 메인컨테이너에 붙이기
        self.container.addWidget(titlebar_widget)
        #step1을 메인컨테이너에 붙이기
        self.container.addWidget(self.step1)


        self.grid = QGridLayout()

        #학습 진행률을 나타낼 프로그레스바 선언
        self.pbar = QProgressBar(self)
        #프로그레스바 퍼센트 ~~~
        self.pbar.setValue(self.pbarValue)

        self.nextBtn = QPushButton("NEXT!", self);
        #self.nextBtn.setDisabled(True)
        self.nextBtn.clicked.connect(self.setFinalUI)

        self.grid.addWidget(self.pbar,0,1)
        self.grid.addWidget(self.nextBtn, 1, 1)
        self.step2 = QGroupBox("step2 : 데이터를 학습합니다.")
        self.step2.setLayout(self.grid)
        
        self.container.addWidget(self.step2)
        self.container.addStretch()
        
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
        print("그렇다면 이건 언제나오냐")

        
    def gkrtmq(self):
        
        """
        데이터 전 처리
        """
       
        # train, test 데이터 읽기
        train_data = self.read_data('ratings_train.txt')[:5]
        test_data = self.read_data('ratings_test.txt')[:5]

        self.pbarValue = 5
        self.pbar.setValue(self.pbarValue)


        print( " 1 " )
        
        # Req 1-1-2. 문장 데이터 토큰화
        # train_docs, test_docs : 토큰화된 트레이닝, 테스트  문장에 label 정보를 추가한 list


        train_docs = [(self.tokenize(i[1]), i[2]) for i in train_data]
        test_docs = [(self.tokenize(i[1]), i[2]) for i in test_data]
        self.pbarValue = 15
        self.pbar.setValue(self.pbarValue)

        time.sleep(1)
        print( " 2 " )
        
        # Req 1-1-3. word_indices 초기화
        self.word_indices = {}

        # Req 1-1-3. word_indices 채우기
        for n_data in train_docs:
            # 품사까지 dict화
            for cnt in n_data[0]:
                if not (self.word_indices.get(cnt)):
                    self.word_indices[cnt] = len(self.word_indices) + 1
            # 문자만 dict화
            # n_data = n_data.split('/')[0]
            # if not (word_indices.get(n_data)):
            #     word_indices[n_data] = len(word_indices) + 1
        # print(word_indices)

        self.pbarValue = 25
        self.pbar.setValue(self.pbarValue)


        time.sleep(1)
        print( " 3 " )

        
        # Req 1-1-4. sparse matrix(희소행렬 = 거의 0으로 채워지고 몇개의 값만 값이 존재) 초기화
        # X: train feature data
        # X_test: test feature data
        self.X = lil_matrix((len(train_data), len(self.word_indices) + 1))
        self.X_test = lil_matrix((len(test_data), len(self.word_indices) + 1))

        self.pbarValue = 27
        self.pbar.setValue(self.pbarValue)

        time.sleep(1)
        print( " 4 " )
        
        # 평점 label 데이터가 저장될 Y 행렬 초기화
        # Y: train data label
        # Y_test: test data label
        self.Y = np.zeros((len(train_data)))
        self.Y_test = np.zeros(((len(test_data))))

        self.pbarValue = 28
        self.pbar.setValue(self.pbarValue)

        # Req 1-1-5. one-hot 임베딩
        # X,Y 벡터값 채우기
        for n in range(len(train_docs)):
            for token in train_docs[n][0]:
                indices = self.word_indices.get(token)
                if indices:
                    self.X[n, indices] = 1
            self.Y[n] = train_docs[n][1]

        for n in range(len(test_docs)):
            for token in test_docs[n][0]:
                indices = self.word_indices.get(token)
                if indices:
                    self.X_test[n, indices] = 1
            self.Y_test[n] = test_docs[n][1]

        self.pbarValue = 37
        self.pbar.setValue(self.pbarValue)

        print( " 5 " )
        
        #=================================================================================================

        # Req 1-2-1. Naive bayes model 학습
        self.clf = MultinomialNB()
        self.pbarValue = 48
        self.pbar.setValue(self.pbarValue)
        self.clf.fit(self.X, self.Y)
        self.pbarValue = 52
        self.pbar.setValue(self.pbarValue)
        # Req 1-2-2. Logistic regression model 학습
        self.clf2 = LogisticRegression()
        self.pbarValue = 73
        self.pbar.setValue(self.pbarValue)
        self.clf2.fit(self.X, self.Y)
        self.pbarValue = 76
        self.pbar.setValue(self.pbarValue)
        # Req 2-3-3. 새로운 학습 모델 사용
        self.knn = KNeighborsClassifier(n_neighbors=2)
        self.pbarValue = 97
        self.pbar.setValue(self.pbarValue)
        self.knn.fit(self.X, self.Y)
        self.pbarValue = 100
        self.pbar.setValue(self.pbarValue)
        self.nextBtn.setEnabled(True)
            

    def setFinalUI(self):
        self.resize(600, 800)
        self.setFixedSize(600, 800)
        self.center()
        self.step1.deleteLater();
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
        

##        """
##        테스트 파트
##        """
##
##        # Req 1-3-1. 문장 데이터에 따른 예측된 분류값 출력
##        print("Naive bayesian classifier example result: {}, {}".format(test_data[3][1], clf.predict(X_test[3])))
##        print("Logistic regression exampleresult: {}, {}".format(test_data[3][1], clf2.predict(X_test[3])))
##        print("K Neighbors classifier example result: {}, {}".format(test_data[3][1], knn.predict(X_test[3])))
##
##        # Req 1-3-2. 정확도 출력
##        print("Naive bayesian classifier accuracy: {}".format(clf.score(X_test, Y_test)))
##        print("Logistic regression accuracy: {}".format(clf2.score(X_test, Y_test)))
##        print("K Neighbors classifier accuracy: {}".format(knn.score(X_test, Y_test)))


    def testData(self):
        #사용자가 실험하고 싶은 문장
        testData = self.inputData.text();

        #TODO :: 원래라면, 학습모델에 데이터를 넣고 결과와 정확도를 뽑아내야함.
        #임의데이터
        self.userTestCnt = self.userTestCnt+1;
        self.userTestres[0].append((self.userTestCnt + 0) * self.userTestCnt)
        self.userTestres[1].append((self.userTestCnt + 1) * self.userTestCnt)
        self.userTestres[2].append((self.userTestCnt + 2) * self.userTestCnt)
        print( testData )
        
        pp = self.preprocess(testData)
        
        print("처리된 데이터 :",pp)
        
        self.outputData1.setText("대략 바뀐 텍스트1" + self.classify1(pp) )
        self.outputData2.setText("대략 바뀐 텍스트2" + self.classify2(pp) )
        self.outputData3.setText("대략 바뀐 텍스트3" + self.classify3(pp) )

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
