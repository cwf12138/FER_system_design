import cv2
import sys
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from recognition_camera import predict_expression
# 加载人脸检测器和表情分类器
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#emotion_classifier = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'emotion_net.caffemodel')

class VideoStream(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Video Stream")

        # 创建一个QLabel控件来显示视频帧
        self.label = QLabel(self)
        self.label.resize(640, 480)

        # 设置OpenCV捕获对象来读取摄像头视频流
        self.capture = cv2.VideoCapture(0)

        # 创建一个定时器，每隔10毫秒更新一次视频帧
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def update_frame(self):
        # 从OpenCV捕获对象中读取一帧
        frame=predict_expression()
        
        ''' ret, frame = self.capture.read()

        if ret:
            # 将图像转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 检测人脸
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # 对于每个检测到的人脸
            for (x,y,w,h) in faces:
                # 将人脸裁剪出来，并调整大小以符合表情分类器的输入大小
                face = cv2.resize(gray[y:y+h, x:x+w], (48, 48))

                # 将人脸输入表情分类器中进行分类
                blob = cv2.dnn.blobFromImage(face, 1./255., (48, 48))
                emotion_classifier.setInput(blob)
                emotion_probs = emotion_classifier.forward()

                # 获取表情分类器的输出，并根据概率最大的类别来判断表情
                emotion = np.argmax(emotion_probs)
                if emotion == 0:
                    emotion_text = 'angry'
                elif emotion == 1:
                    emotion_text = 'disgust'
                elif emotion == 2:
                    emotion_text = 'fear'
                elif emotion == 3:
                    emotion_text = 'happy'
                elif emotion == 4:
                    emotion_text = 'sad'
                elif emotion == 5:
                    emotion_text = 'surprise'
                else:
                    emotion_text = 'neutral'

                # 在原始图像上绘制人脸和表情分类结果
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, emotion_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            '''
                       # 将OpenCV图像转换为QImage格式
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()

            # 将QImage格式转换为QPixmap格式，以便在QLabel控件中显示
        pixmap = QPixmap.fromImage(image)

            # 调整QPixmap控件大小以适应QLabel控件
        self.label.setPixmap(pixmap.scaled(self.label.width(), self.label.height(), aspectRatioMode=1))

        #else:
            # 如果未能从OpenCV捕获对象中读取帧，则停止定时器
            #self.timer.stop()

if __name__ == '__main__':
    # 创建PyQt5应用程序对象
    app = QApplication(sys.argv)

    # 创建VideoStream对象并显示
    video_stream = VideoStream()
    video_stream.show()

    # 运行应用程序并等待退出
    sys.exit(app.exec_())

