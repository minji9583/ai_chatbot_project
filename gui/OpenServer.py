import sys
import os
import pickle
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt, QThread
from PyQt5 import QtWidgets, QtCore, QtGui
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
import time

##### 서버 오픈 부분
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
from flask import Flask
from flask import request
from flask_restful import Resource, Api

class Data(Resource):
    def get(self, text):
        ans = classify(text)
        return {'result': ans}



def shutdown_server(self):
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def tokenize(self,doc):
    tt = okt.pos(doc, norm=True, stem=True)
    return ['/'.join(t) for t in tt]


def preprocess(self,text):
    vocas = tokenize(text)
    X = [0] * (len(word_indices) + 1)
    for voca in vocas:
        indices = word_indices.get(voca)
        if indices:
            X[indices] = 1
    X = [X]
    return np.array(X)

def classify(self,text):
    
    data = preprocess(text)

    result1 = naive.predict(data)[0]
    result2 = logi.predict(data)[0]
    result3 = knn.predict(data)[0]

    if result1 + result2 + result3 >= 2:
        return "긍정"
    else:
        return "부정"



    
class FlaskThread(QThread):
    def __init__(self, application):
        QThread.__init__(self)
        self.application = application
        self.runStatus = False;

    def __del__(self):
        self.wait()
        
    def stop(self):
        self.runStatus = True;
        
    def run(self):
        self.application.run(port=5000)
        

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
        self.resize(300, 150)
        self.setFixedSize(300, 150)
        self.webapp = FlaskThread(Flaskapp)
        
        self.container = QtWidgets.QVBoxLayout(self)
        self.container.setContentsMargins(1, 1, 1, 1)
        
        self.setLayout(self.container)
        self.initUI()


        with open('model.clf', 'rb') as f:
            model = pickle.load(f)

        self.word_indices = model.get_word_indices()
        self.naive = model.get_naive_model()
        self.logi = model.get_logistic_model()
        self.knn = model.get_k_neighbors_model()

        self.okt = Okt()

    
    def initUI(self): 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #프레임을 없애고

        #타이틀 바 설정
        titlebar_widget =  MainTitleBar(self)
        #타이틀 바에 고유 아이디 등록(qss에 사용)
        titlebar_widget.setObjectName("windowTitle")
        
        #컨텐트 박스에 위젯들 붙이기

        self.contentBox = QtWidgets.QHBoxLayout(self)
        self.container.setAlignment(Qt.AlignTop)

        self.statusPNG = QLabel(self)
        self.pixmap = QtGui.QPixmap("img/off.png")
        self.statusPNG.resize(30,30)
        self.statusPNG.setPixmap(self.pixmap.scaled(self.statusPNG.size(), QtCore.Qt.IgnoreAspectRatio))

        self.statusLabel = QLabel("　SERVER CLOSED　　　　　　　　")
        self.onoffBtn = QPushButton("서버 실행", self)
        self.onoffBtn.clicked.connect(self.ServerOn)
        
        #타이틀바 위젯을 메인컨테이너에 붙이기
        self.container.addWidget(titlebar_widget)
        self.contentBox.addWidget(self.statusPNG)
        self.contentBox.addWidget(self.statusLabel)
        self.contentBox.addWidget(self.onoffBtn)
        self.contentBox.setContentsMargins(20, 0, 20, 0) # 좌 상 우 하
        self.container.addLayout(self.contentBox)
        self.center()
        self.show()

    def ServerOn(self):
        self.pixmap = QtGui.QPixmap("img/on.png")
        self.statusPNG.setPixmap(self.pixmap.scaled(self.statusPNG.size(), QtCore.Qt.IgnoreAspectRatio))
        self.onoffBtn.setText("중지하기")
        self.statusLabel.setText("　running...　　　　　　")
        self.onoffBtn.clicked.connect(self.ServerOff)        
        self.webapp.start()
       
        
    def ServerOff(self):
        self.pixmap = QtGui.QPixmap("img/off.png")
        self.statusPNG.setPixmap(self.pixmap.scaled(self.statusPNG.size(), QtCore.Qt.IgnoreAspectRatio))
        self.onoffBtn.setText("시작하기")
        self.statusLabel.setText("　closed　　　　　　　　")
        self.onoffBtn.clicked.connect(self.ServerOn)
        self.webapp.stop()
        
    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        print("select : " + fname[0])
        self.sFile.setText(fname[0])

    def showPathDialog(self):
        pname = QFileDialog.getExistingDirectory()
        print("select : " + pname)
        self.sPath.setText(pname)

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

        label = QtWidgets.QLabel("서버 실행기")
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
    qtapp = QApplication(sys.argv)
    Flaskapp = Flask(__name__)
    api = Api(Flaskapp)
    api.add_resource(Data, '/<string:text>')
    webapp = FlaskThread(Flaskapp)
    ex = MyApp()
    sys.exit(qtapp.exec_())
