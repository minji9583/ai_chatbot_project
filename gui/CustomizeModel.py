import sys
import pickle
from PyQt5.QtWidgets import \
    QApplication, QWidget, QDesktopWidget, QGridLayout, QLabel, QPushButton, QFileDialog, QLineEdit

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.sPath = QLabel("선택한 경로가 없습니다.")
        self.sFile = QLabel("선택한 파일이없습니다.")
        self.filename = QLineEdit()
        
        selectRouteBtn = QPushButton("경로 선택", self)
        selectRouteBtn.clicked.connect(self.showPathDialog)
        selectFileBtn = QPushButton("파일 선택", self)
        selectFileBtn.clicked.connect(self.showFileDialog)
        startBtn = QPushButton("학습 시작", self)
        startBtn.clicked.connect(self.makeCM)

        grid.addWidget(QLabel('저장 경로 :'), 0, 0)
        grid.addWidget(self.sPath, 0, 1)
        grid.addWidget(selectRouteBtn, 0,2)

        grid.addWidget(QLabel('저장할 파일 이름 :'), 1, 0)
        grid.addWidget(self.filename, 1, 1)
        grid.addWidget(QLabel('.clf'), 1, 2)

        grid.addWidget(QLabel('학습 데이터 선택 :'), 2, 0)
        grid.addWidget(self.sFile, 2, 1)
        grid.addWidget(selectFileBtn, 2,2)

        grid.addWidget(startBtn,3,1)

        self.setWindowTitle('학습장치')
        self.resize(800, 520)
        self.center()
        self.show()

    def makeCM(self):
        res = "this is result!" #학습 결과
        fname = self.filename.text() #사용자가 입력한 저장 파일 이름
        
        #TODO 추후clf로 확장자를 바꿔야함. 실험을 위해 txt로 남겨둠
        path = self.sPath.text() +"//" + fname + ".txt"
        with open(path, 'wb') as f:
            pickle.dump(res, f)

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        print(fname[0])
        self.sFile.setText(fname[0])

    def showPathDialog(self):
        pname = QFileDialog.getExistingDirectory()
        print(pname)
        self.sPath.setText(pname)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())