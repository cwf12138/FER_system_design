import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import  QLineEdit, QTextEdit, QStackedWidget, QTabWidget,QMainWindow,QFrame
from qt_material import apply_stylesheet
from recognition_camera import Camera,load_model
class UsageRecord(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 添加组件
        date_label = QLabel('日期：')
        date_edit = QLineEdit()
        user_label = QLabel('用户：')
        user_edit = QLineEdit()
        action_label = QLabel('操作：')
        action_edit = QLineEdit()

        # 创建布局管理器
        hbox1 = QHBoxLayout()
        hbox1.addWidget(date_label)
        hbox1.addWidget(date_edit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(user_label)
        hbox2.addWidget(user_edit)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(action_label)
        hbox3.addWidget(action_edit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        # 设置布局管理器
        self.setLayout(vbox)


class FaceRecognition(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 添加组件
        img_label = QLabel('显示图片区域')
        result_label = QLabel('显示识别结果区域')
        bar_label = QLabel('显示柱状图区域')

        # 创建布局管理器
        vbox = QVBoxLayout()
        vbox.addWidget(img_label)
        vbox.addWidget(result_label)
        vbox.addWidget(bar_label)

        # 设置布局管理器
        self.setLayout(vbox)


class CameraRecognition(QWidget):
    def __init__(self,model):
        super().__init__()
        self.model=model
        self.initUI()

    def initUI(self):
        # 添加组件
        camera_label = QLabel('显示摄像头获取的图像区域')
        camera_widget=Camera(self.model)
        camera_box=camera_widget.vbox
        bar_label = QLabel('显示柱状图区域')
        desc_label = QLabel('显示说明区域')
        separator_line_v = QFrame()
        separator_line_v.setFrameShape(QFrame.VLine)
        separator_line_v.setFrameShadow(QFrame.Sunken)
        separator_line_h = QFrame()   #separator_line_h.setLineWidth(3)#separator_line_h.setMidLineWidth(3) 增加宽度
        separator_line_h.setFrameShape(QFrame.HLine)
        separator_line_h.setFrameShadow(QFrame.Sunken)
        #qbtn=QPushButton("push it")
        # 创建布局管理器
        hbox = QHBoxLayout()
        vbox_left = QVBoxLayout()
        vbox_left.addWidget(camera_label)
        #vbox_left.addWidget(qbtn)
        hbox.addLayout(camera_box)
        hbox.addWidget(separator_line_v)

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(bar_label)
        vbox_right.addWidget(separator_line_h)
        vbox_right.addWidget(desc_label)
        hbox.addLayout(vbox_right)

        # 设置布局管理器
        self.setLayout(hbox)


class VideoRecognition(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 添加组件
        video_label = QLabel('显示视频区域')
        bar_label = QLabel('显示柱状图区域')
        desc_label = QLabel('显示说明区域')
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        separator_line_h = QFrame()
        #separator_line_h.setLineWidth(3)
        #separator_line_h.setMidLineWidth(3) 
        separator_line_h.setFrameShape(QFrame.HLine)
        separator_line_h.setFrameShadow(QFrame.Plain)

        # 创建布局管理器
        hbox = QHBoxLayout()
        vbox_left = QVBoxLayout()
        vbox_left.addWidget(video_label)
        #vbox_left.addWidget(separator_line)
        hbox.addLayout(vbox_left)
        hbox.addWidget(separator_line)

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(desc_label)
        vbox_right.addWidget(separator_line_h)
        vbox_right.addWidget(bar_label)
        hbox.addLayout(vbox_right)

        # 设置布局管理器
        self.setLayout(hbox)

#Qwidget
class MainWindow(QMainWindow):
    def __init__(self,model):
        super().__init__()
        self.model=model
        self.initUI()

    def initUI(self):
        # 添加组件
        main_widget=QWidget()
        title_label = QLabel('人脸表情识别系统')
        face_recognition_btn = QPushButton('基于图片的表情识识')
        camera_recognition_btn = QPushButton('基于摄像头的表情识别')
        video_recognition_btn = QPushButton('基于视频的表情识别')
        usage_record_btn = QPushButton('查看使用记录')
        # 创建堆叠窗口和页面
        stacked_widget = QStackedWidget()
        #四个功能界面
        face_recognition_page = FaceRecognition()
        camera_recognition_page = CameraRecognition(self.model)
        video_recognition_page = VideoRecognition()
        usage_record_page = UsageRecord()
        #添加到堆叠窗口里
        stacked_widget.addWidget(face_recognition_page)
        stacked_widget.addWidget(camera_recognition_page)
        stacked_widget.addWidget(video_recognition_page)
        stacked_widget.addWidget(usage_record_page)

        # 创建标签页
        tab_widget = QTabWidget()
        tab_widget.addTab(stacked_widget, '功能')  #当前页面
        tab_widget.addTab(QTextEdit(), '帮助')


        # 创建布局管理器

        '''vbox = QVBoxLayout()
        vbox.addWidget(title_label, alignment=Qt.AlignCenter)
        vbox.addWidget(face_recognition_btn)
        vbox.addWidget(camera_recognition_btn)
        vbox.addWidget(video_recognition_btn)
        vbox.addWidget(usage_record_btn)
        vbox.addWidget(tab_widget)'''
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(face_recognition_btn)
        nav_layout.addWidget(camera_recognition_btn)
        nav_layout.addWidget(video_recognition_btn)
        nav_layout.addWidget(usage_record_btn)
        #nav_layout.addWidget(tab_widget)
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(tab_widget)


        # 设置布局管理器
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 信号槽连接
        face_recognition_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(face_recognition_page))
        camera_recognition_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(camera_recognition_page))
        video_recognition_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(video_recognition_page))
        usage_record_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(usage_record_page))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    model=load_model()
    window = MainWindow(model)
    window.show()
    sys.exit(app.exec_())
