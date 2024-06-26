import cv2
import sys
import requests,json,os,time
from datetime import date,datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QImage, QPixmap,QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,QDesktopWidget,QHBoxLayout, QVBoxLayout, QPushButton, QWidget,QFrame,QSizePolicy,QStackedLayout,QGraphicsView
from PyQt5.QtCore import QObject, pyqtSignal,Qt, QTimer,QSize,QCoreApplication,QRect
from matplotlib.figure import Figure
from recognition_camera import load_model
from qt_material import apply_stylesheet
from qtchart_widget import BarChart
matplotlib.use("Qt5Agg")
sys.path.append('../')

xemotions = ['anger', 'disgust', 'fear', 'happy', 'sad', 'surprised', 'neutral', 'contempt']
from recognition import *
class Picture(QWidget):
    def __init__(self, model,number):
        super().__init__()
        self.model = model
        self.possibility=[0,0,0,0,0,0,0,0]
        self.filename=''
        self.number=number
        self.emotion='no'
        self.setup_ui()
        

    def setup_ui(self):
        self.setObjectName("Form")
        self.resize(1200, 800)   #大小
        # 原图无图时显示的label      #懂了，就是左上部分那个深灰色小方框
        self.label_raw_pic = QLabel("NULL")
        #self.label_raw_pic.setGeometry(QRect(10, 30, 320, 240))
        self.label_raw_pic.setStyleSheet("background-color:#bbbbbb;")
        self.label_raw_pic.setFixedSize(320, 270)  #240
        self.label_raw_pic.setAlignment(Qt.AlignCenter)      #居中
        #self.label_raw_pic.setObjectName("label_raw_pic")
        # 结果图无图时显示的label      #懂了，就是左下部分那个深灰色小方框
        self.label_result_pic = QLabel("NULL")
        #self.label_raw_pic.setGeometry(QRect(10, 30, 320, 240))
        self.label_result_pic.setStyleSheet("background-color:#bbbbbb;")
        self.label_result_pic.setFixedSize(320, 270) #240
        self.label_result_pic.setAlignment(Qt.AlignCenter)      #居中

        # 原图下方分割线
        self.line1 = QFrame()
        #self.line1.setGeometry(QtCore.QRect(340, 30, 20, 431))
        self.line1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        #self.line1.setObjectName("line1")
        # 作者说明label
        self.label_designer = QLabel('no')

        #self.label_designer.setGeometry(QtCore.QRect(20, 700, 180, 40))
        self.label_designer.setStyleSheet("font-size: 20px;") #修改字体样式
        #self.label_designer.setFont(QFont("Arial", 18, QFont.Bold))   
        font = QtGui.QFont()
        font.setPointSize(10)
        #self.label_designer.setFont(font)
        #self.label_designer.setObjectName("label_designer")
        # 结果布局设置
        self.layout_widget = QWidget()
        #self.layout_widget.setGeometry(QRect(10, 310, 320, 240))
        #self.layout_widget.setObjectName("layoutWidget")
        #self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        #self.horizontal_layout.setObjectName("verticalLayout")
        # 右侧水平线
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        #self.line2.setObjectName("line2")
        #self.horizontal_layout.addWidget(self.line1)
        self.horizontal_layout =QHBoxLayout()
        #self.horizontal_layout.setObjectName("horizontalLayout")
        self.pushButton_select_img = QPushButton()
        #self.pushButton_select_img.setObjectName("pushButton_2")
        #self.horizontal_layout.addWidget(self.pushButton_select_img)
        self.graphicsView =  QGraphicsView()
        #self.graphicsView.setGeometry(QtCore.QRect(360, 210, 800, 500))
        #self.graphicsView.setObjectName("graphicsView")
        self.label_result = QLabel()
        #self.label_result.setGeometry(QRect(361, 21, 71, 16))
        #self.label_result.setObjectName("label_result")
        self.label_emotion = QLabel()
        self.label_emotion.setStyleSheet("font-size: 20px;") #修改字体样式
        #self.label_emotion.setGeometry(QRect(715, 21, 71, 16))
        #self.label_emotion.setObjectName("label_emotion")
        self.label_emotion.setAlignment(Qt.AlignCenter)
        self.label_bar = QLabel()
        #self.label_bar.setGeometry(QRect(720, 170, 80, 180))
        #self.label_bar.setObjectName("label_bar")
        self.line =QFrame()
        #self.line.setGeometry(QRect(361, 150, 800, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        #self.line.setObjectName("line")
        self.label_rst = QLabel()
        #self.label_rst.setGeometry(QRect(700, 50, 100, 100))
        self.label_rst.setAlignment(Qt.AlignCenter)
        #self.label_rst.setObjectName("label_rst")

        self.pushButton_select_img.clicked.connect(self.open_file_browser)
        self.retranslate_ui()
        self.barchart=BarChart(xemotions,self.possibility)
        self.vbox_left=QVBoxLayout()  #左边垂直布局
        self.vbox_right=QVBoxLayout()  #右边垂直布局
        self.vbox_left.addWidget(self.label_raw_pic)
        self.vbox_left.addWidget(self.line2)
        self.vbox_left.addWidget(self.pushButton_select_img)
        self.vbox_left.addWidget(self.line2)
        self.vbox_left.addWidget(self.label_result_pic)   #结果图
        self.vbox_left.addStretch()   #可以将self.label_designer 移动到左下角
        self.vbox_left.addWidget(self.label_designer)
        #self.vbox_left.addWidget(self.line2)
        self.horizontal_layout.addLayout(self.vbox_left)
        self.horizontal_layout.addWidget(self.line1)
        self.vbox_right.addWidget(self.label_result)
        self.vbox_right.addWidget(self.label_emotion)
        self.vbox_right.addWidget(self.label_rst)
        self.vbox_right.addWidget(self.line2)
        #self.vbox_right.addWidget(self.line2)
        self.vbox_right.addWidget(self.label_bar)
        self.vbox_right.addWidget(self.barchart)
        self.horizontal_layout.addLayout(self.vbox_right)
        self.setLayout(self.horizontal_layout)
        #上方部分就是初始化ui界面，将整个方框的布局弄出来

    def retranslate_ui(self):
        self.label_raw_pic.setText("O(∩_∩)O")
        self.label_result_pic.setText("^-^")
        self.label_designer.setText("designed by gzu-cwf")
        self.pushButton_select_img.setText("选择图像")
        self.label_result.setText("识别结果")
        self.label_emotion.setText("null")
        self.label_bar.setText( "概率直方图")
        self.label_rst.setText("Result")
       
    #添加文字信息
    def open_file_browser(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(
        caption="选取图片", directory="./input/test/",filter="All Files (*);;Text Files (*.txt)")
        if file_name is not None and file_name != "":
            self.filename=file_name
            self.show_raw_img(file_name)  
            emotion, possibility = predict_expression(file_name, self.model)  
            file_name_result='./output/rst.png'
            self.show_result_img(file_name_result)
            self.emotion=emotion
            self.possibility=possibility
            self.vbox_right.removeWidget(self.barchart)
            self.barchart=BarChart(xemotions,list(self.possibility))
            self.vbox_right.addWidget(self.barchart)
            self.show_results(emotion, possibility) 
            url='http://127.0.0.1:5000/add_picture_record/'
            data={"number":self.number,'result':self.emotion,'picture_address':self.filename}
            response = requests.post(url, json=data)
    def show_results(self, emotion, possibility):  
        self.label_emotion.setText(QtCore.QCoreApplication.translate("Form", emotion))
        if emotion != 'no':
            img = cv2.imread('./assets/icons/' + str(emotion) + '.png')    
            frame = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (100, 100))  
            self.label_rst.setPixmap(QtGui.QPixmap.fromImage(
                QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], 3 * frame.shape[1],
                             QtGui.QImage.Format_RGB888)))
        else:
            self.label_rst.setText(QtCore.QCoreApplication.translate("Form", "no result"))  

    def show_raw_img(self, filename):   #这个部分就是显示图片并更改了大小   #?这个部分是值得参考的，hh
        img = cv2.imread(filename)
        frame = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (320, 270)) #修改大小  320 240   320 280
        self.label_raw_pic.setPixmap(QtGui.QPixmap.fromImage(
                    QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], 3 * frame.shape[1],QtGui.QImage.Format_RGB888)))  
                                        #这里相当于就是显示图片
    def show_result_img(self, filename):   #这个部分就是显示图片并更改了大小  结果图
        img = cv2.imread(filename)
        frame = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (320, 270)) #修改大小  320 240 320 280
        self.label_result_pic.setPixmap(QtGui.QPixmap.fromImage(
                    QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], 3 * frame.shape[1],QtGui.QImage.Format_RGB888)))    #这里相当于就是显示图片
    def show_test_img(self,filename):
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaled(320, 270) 
        self.label_result_pic.setPixmap(pixmap)
   
        # 显示直方图
       # self.show_bars(list(possibility))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    model = load_model()
    picture=Picture(model)
    picture.show()
    sys.exit(app.exec_())
