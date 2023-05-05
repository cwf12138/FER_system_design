"""
author: Zhou Chen
datetime: 2019/6/20 15:44
desc: 利用摄像头实时检测
"""
import os
import argparse
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
sys.path.append('../')
import cv2
import numpy as np
from model import CNN2, CNN3
from utils import index2emotion, cv2_img_add_text
from blazeface import blaze_detect


from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,QDesktopWidget,QHBoxLayout, QVBoxLayout, QPushButton, QWidget,QFrame,QSizePolicy,QStackedLayout
from PyQt5.QtCore import QObject, pyqtSignal,Qt, QTimer,QSize,QCoreApplication
from qt_material import apply_stylesheet
from qtchart_widget import BarChart


parser = argparse.ArgumentParser()
parser.add_argument("--source", type=int, default=0, help="data source, 0 for camera 1 for video")
parser.add_argument("--video_path", type=str, default=None)
opt = parser.parse_args()

if opt.source == 1 and opt.video_path is not None:
    filename = opt.video_path     #这里判断是否在线还是离线操作
else:
    filename = None

emotions_trans = {
        'anger': '发怒',
        'disgust': '厌恶',
        'fear': '恐惧',
        'happy': '开心',
        'sad': '伤心',
        'surprised': '惊讶',
        'neutral': '中性',
        'contempt': '蔑视',
        'no':'无',

}
xemotions = ['anger', 'disgust', 'fear', 'happy', 'sad', 'surprised', 'neutral', 'contempt']
def load_model():
    """
    加载本地模型
    :return:
    """
    model = CNN3()
    model.load_weights('./models/cnn3_best_weights.h5')
    return model


def generate_faces(face_img, img_size=48):
    """
    将探测到的人脸进行增广
    :param face_img: 灰度化的单个人脸图
    :param img_size: 目标图片大小
    :return:
    """

    face_img = face_img / 255.
    face_img = cv2.resize(face_img, (img_size, img_size), interpolation=cv2.INTER_LINEAR)
    resized_images = list()
    resized_images.append(face_img)
    resized_images.append(face_img[2:45, :])
    resized_images.append(face_img[1:47, :])
    resized_images.append(cv2.flip(face_img[:, :], 1))

    for i in range(len(resized_images)):
        resized_images[i] = cv2.resize(resized_images[i], (img_size, img_size))
        resized_images[i] = np.expand_dims(resized_images[i], axis=-1)
    resized_images = np.array(resized_images)
    return resized_images


#QMainWindow
class Camera(QWidget):
    def __init__(self,model,filename=None, parent=None):
        super().__init__()
        self.title = 'Face Recognition'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.model=model
        self.filename=filename
        self.emotion=[]
        self.result_possibility=[1,2,4,6,1,4,2,2]
        self.label_img=QLabel('img')
        self.label_emotion=QLabel('emotion')
        self.label_chart=QLabel('chart')
        self.setObjectName=("FER")
        #self.video_capture = video_capture
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # 定义一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.predict_expression_test)   
        self.timer.timeout.connect(lambda:self.show_emotion(self.emotion))
        #lambda:child_window.show()
        self.show_emotion(self.emotion)
        # 创建一个标签用于显示视频流
        self.label_video = QLabel(self)
        self.label_video.setAlignment(Qt.AlignCenter)
        bar_label = QLabel('显示柱状图区域')
        desc_label = QLabel('显示说明区域')
        separator_line_v = QFrame()
        separator_line_v.setFrameShape(QFrame.VLine)
        separator_line_v.setFrameShadow(QFrame.Sunken)
        separator_line_h = QFrame()   #separator_line_h.setLineWidth(3)#separator_line_h.setMidLineWidth(3) 增加宽度
        separator_line_h.setFrameShape(QFrame.HLine)
        separator_line_h.setFrameShadow(QFrame.Sunken)
        # 创建一个按钮用于开始/暂停视频流的播放
        self.btn_play_pause = QPushButton("Play", self)
        self.btn_play_pause.clicked.connect(self.play_pause_video)
        # 创建一个按钮用于停止视频流的播放
        self.btn_stop = QPushButton("Stop", self)
        self.btn_stop.clicked.connect(self.stop_video)
        # 创建一个水平布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_play_pause)
        hbox.addWidget(self.btn_stop)

        # 创建一个垂直布局，将标签和水平布局添加进去
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_video)
        vbox.addLayout(hbox)
        vbox.addStretch()

        # 将垂直布局应用于主窗口
        #self.vbox=vbox
        #self.setLayout(vbox)  #这里很关键\
        self.hbox = QHBoxLayout()
        #vbox_left.addWidget(qbtn)
        self.hbox.addLayout(vbox)
        self.hbox.addWidget(separator_line_v)

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(self.label_emotion)
        vbox_right.addWidget(self.label_img)
        vbox_right.addWidget(separator_line_h)
        #self.stackedLayout = QStackedLayout()
        #print(self.result_possibility)
        #生成柱状图表
        #barchart=BarChart(xemotions,list(self.result_possibility))
        #self.barchart=barchart
        #self.vbox_right.addWidget(self.barchart)
        #self.label_chart.setLayout(self.vbox_right)
        vbox_right.addStretch()
        self.hbox.addLayout(vbox_right)
        #hbox.addWidget(self.label_chart)
        self.setLayout(self.hbox)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        # 打开视频流
        #self.cap = cv2.VideoCapture(0)
        self.capture = cv2.VideoCapture(0)  # 指定0号摄像头
        #print(filename)
        #print(self.filename)
        if self.filename:
            self.capture = cv2.VideoCapture(self.filename)
        self.timer.start(30)
        
        #居中显示
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        #self.show()
    def predict_expression_test(self):   #测试暂停键和关闭键是否成功,已成功
        #model = load_model()
        border_color = (0, 0, 0)  # 黑框框
        font_color = (255, 255, 255)  # 白字字
        #if filename:
            #self.capture = cv2.VideoCapture(filename)
        
        _, frame = self.capture.read()  # 读取一帧视频，返回是否到达视频结尾的布尔值和这一帧的图像
            #frame = cv2.cvtColor(cv2.resize(frame, (800, 600)), cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰度化
            # cascade = cv2.CascadeClassifier('./dataset/params/haarcascade_frontalface_alt.xml')  # 检测人脸
            # # 利用分类器识别出哪个区域为人脸
            # faces = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(120, 120))
        emotions = []
        result_possibilities = []
        faces = blaze_detect(frame)
        if faces is not None and len(faces) > 0:
            for (x, y, w, h) in faces:
                face = frame_gray[y: y + h, x: x + w]  # 脸部图片
                faces = generate_faces(face)
                results = self.model.predict(faces)
                result_sum = np.sum(results, axis=0).reshape(-1) #这里也可以加一个概率统计 ，frame 和 possibilities
                label_index = np.argmax(result_sum, axis=0)
                emotion = index2emotion(label_index,'en')  #*这里可以注意一下
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), border_color, thickness=2)
                frame = cv2_img_add_text(frame, emotion, x+30, y+30, font_color, 20)   #*这里也是
                emotions.append(emotion)
                result_possibilities.append(result_sum)
                    # puttext中文显示问题
                    # cv2.putText(frame, emotion, (x + 30, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 4)
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        if len(emotions)!=0:  #修复了emotions列表可能为空并出现IndexError: list index out of range的bug
            self.emotion=emotions[0]
        if len(result_possibilities)!=0:
            self.result_possibility=result_possibilities[0]
        
            # 将 QImage 对象转换为 QPixmap 对象
        #QPixmap类用于绘图设备的图像显示，它可以作为一个QPainterDevice对象，也可以加载到一个控件中，通常是标签或者按钮，用于在标签或按钮上显示图像
        pixmap = QPixmap.fromImage(qImg)    
            # 在标签上显示图像
        self.label_video.setPixmap(pixmap)
        #self.vbox_right.removeWidget(self.barchart)
        #self.barchart=BarChart(xemotions,list(self.result_possibility))
        #self.vbox_right.addWidget(self.barchart)
    def show_emotion(self, emotion):  #展示结果   也是可以借鉴的hh
        # 显示表情名
        if len(emotion)==0:
            emotion='no'
        #print(emotion)
        self.label_emotion.setText(emotions_trans[emotion])
        # 显示emoji
        if emotion != 'no':
            img = cv2.imread('./assets/icons/' + str(emotion) + '.png')    #这里是iemoji表情的路径
            #print()
            frame = cv2.cvtColor(cv2.resize(img, (100,100)), cv2.COLOR_BGR2RGB)  #修改大小
            self.label_img.setPixmap(QPixmap.fromImage(QImage(frame.data, frame.shape[1], frame.shape[0], 3 * frame.shape[1],
                             QImage.Format_RGB888)))
        else:
            self.label_img.setText("no result")  #翻译
        #self.barchart=BarChart(x,list(self.result_possibility))
        #print(self.result_possibility)
        # 显示直方图
    def play_pause_video(self):
        """开始/暂停视频流的播放"""
        if not self.timer.isActive():
            self.timer.start(30)
            self.btn_play_pause.setText("Pause")
        else:
            self.timer.stop()
            self.btn_play_pause.setText("Play")

    def stop_video(self):
        """停止视频流的播放"""
        self.timer.stop()
        self.btn_play_pause.setText("Play")
        self.label_video.clear()
        self.label_emotion.setText("emotion")
        self.label_img.setText("img")

    def closeEvent(self, event):
        # 触发信号
        # 关闭窗口
        self.capture.release()
        #cv2.destroyAllWindows()
        event.accept()




    

def predict_expression():
    """
    实时预测
    :return:
    """
    # 参数设置
    model = load_model()

    border_color = (0, 0, 0)  # 黑框框
    font_color = (255, 255, 255)  # 白字字
    capture = cv2.VideoCapture(0)  # 指定0号摄像头
    app = QApplication(sys.argv)
    ex = Camera(capture)
    if filename:
        capture = cv2.VideoCapture(filename)

    while True:
        _, frame = capture.read()  # 读取一帧视频，返回是否到达视频结尾的布尔值和这一帧的图像
        #frame = cv2.cvtColor(cv2.resize(frame, (800, 600)), cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰度化
        # cascade = cv2.CascadeClassifier('./dataset/params/haarcascade_frontalface_alt.xml')  # 检测人脸
        # # 利用分类器识别出哪个区域为人脸
        # faces = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=1, minSize=(120, 120))
        faces = blaze_detect(frame)
        # 如果检测到人脸
        if faces is not None and len(faces) > 0:
            for (x, y, w, h) in faces:
                face = frame_gray[y: y + h, x: x + w]  # 脸部图片
                faces = generate_faces(face)
                results = model.predict(faces)
                result_sum = np.sum(results, axis=0).reshape(-1) #这里也可以加一个概率统计 ，frame 和 possibilities
                label_index = np.argmax(result_sum, axis=0)
                emotion = index2emotion(label_index)  #*这里可以注意一下
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), border_color, thickness=2)
                frame = cv2_img_add_text(frame, emotion, x+30, y+30, font_color, 20)   #*这里也是
                # puttext中文显示问题
                # cv2.putText(frame, emotion, (x + 30, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 4)
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        # 将 QImage 对象转换为 QPixmap 对象
        pixmap = QPixmap.fromImage(qImg)
        # 在标签上显示图像
        ex.label_video.setPixmap(pixmap)

        # 每 25 毫秒刷新一次界面
        #QApplication.processEvents()
        #cv2.waitKey(25)
        #cv2.imshow("expression recognition(press esc to exit)", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # 利用人眼假象，这里是展示环节
        #frame=cv2.cvtColor(frame,cv2.COLOR_HSV2BGR)
        #return frame
        key = cv2.waitKey(30)  # 等待30ms，返回ASCII码
                                         
        # 如果输入esc则退出循环
        if key == 27:
            break
    #capture.release()  # 释放摄像头
    #cv2.destroyAllWindows()  # 销毁窗口
    #sys.exit(app.exec_())
    #return frame
    app.exec_()

if __name__ == '__main__':
    #predict_expression()
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    model = load_model()  #导入模型，提出来，不然循环每次都导入会报内存的
    ex = Camera(model)
    ex.show()
    app.exec_()