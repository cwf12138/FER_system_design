import sys,cv2,time,requests,os
from PyQt5.QtCore import Qt ,pyqtSlot,pyqtSignal
from PyQt5.QtGui import QPixmap,QIcon,QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import  QLineEdit, QTextEdit, QStackedWidget, QTabWidget,QMainWindow,QFrame
from qt_material import apply_stylesheet
from recognition_camera import Camera,load_model
from recognition_picture import Picture
from recognition_record import Camera_table,Video_table,Picture_table
from qtupload import Videoupload
from your_profile import UserDropDown
from return_to_home import Return_to_home
from login_and_register import LoginWindow,RegisterWindow
sys.path.append('../')
from getdata import get_picture_usage_record,get_camera_usage_record,get_video_usage_record
class UsageRecord(QWidget):
    def __init__(self,number):
        super().__init__()
        self.number=number
        self.initUI()

    def initUI(self):
        # 添加组件
        data_pciture=get_picture_usage_record(self.number)
        data_camera=get_camera_usage_record(self.number)
        data_video= get_video_usage_record(self.number)
        self.tab_widget=QTabWidget()
        self.tab_widget.addTab(Picture_table(data_pciture),'picture')
        self.tab_widget.addTab(Camera_table(data_camera),'camera')
        self.tab_widget.addTab(Video_table(data_video),'video')
        main_layout=QHBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)
        


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

#Qwidget
class CameraRecognition(Camera):
    def __init__(self,model):
        super().__init__(self,model)
        self.model=model
        self.initUI()

    def initUI(self):
        # 添加组件
        camera_label = QLabel('显示摄像头获取的图像区域')
        #camera_widget=Camera(self.model)
        #camera_box=camera_widget.vbox
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
        hbox.addLayout(vbox_left)
        hbox.addWidget(separator_line_v)

        vbox_right = QVBoxLayout()
        vbox_right.addWidget(bar_label)
        vbox_right.addWidget(separator_line_h)
        vbox_right.addWidget(desc_label)
        hbox.addLayout(vbox_right)

        # 设置布局管理器
        #self.setLayout(hbox)


class VideoRecognition(QWidget):
    def __init__(self,model):
        super().__init__()
        self.model=model
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
        cam=Camera(self.model)
        hbox.addWidget(cam)

        # 设置布局管理器
        self.setLayout(hbox)

#Qwidget
class MainWindow(QMainWindow):
    def __init__(self,model):
        super().__init__()
        self.model=model
        self.filename=''
        self.number='18212139396'
        self.initUI()

    def initUI(self):
        # 添加组件
        self.resize(1000,800)
        self.setWindowIcon(QIcon("./avatar3.jpg"))  # 设置窗口图标
        #self.setWindowIcon(QIcon())  #设置窗口图标为空
        self.setWindowTitle(" ")
        #self.setWindowFlags(Qt.FramelessWindowHint)
        main_widget=QWidget()
        title_label = QLabel('人脸表情识别系统')
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        face_recognition_btn = QPushButton('基于图片的表情识别')
        camera_recognition_btn = QPushButton('基于摄像头的表情识别')
        video_recognition_btn = QPushButton('基于视频的表情识别')
        usage_record_btn = QPushButton('查看使用记录')
        # 创建堆叠窗口和页面
        self.stacked_widget = QStackedWidget()
        #四个功能界面
        self.face_recognition_page = Picture(self.model,self.number)
        #self.camera_recognition_page = Camera(self.model)
        self.camera_recognition_page=QWidget()
        self.camera_recognition_page.setVisible(False)
        self.video_recognition_page_load = Videoupload(self.model)
        #camera_recognition_page = Camera(self.model)
        #self.video_recognition_page = VideoRecognition(self.model)
        self.video_recognition_page=QWidget()
        self.usage_record_page = UsageRecord(self.number)
        #添加到堆叠窗口里
        self.stacked_widget.addWidget(self.face_recognition_page)
        self.stacked_widget.addWidget(self.usage_record_page)
        #self.stacked_widget.addWidget(self.camera_recognition_page)
        self.stacked_widget.addWidget(self.video_recognition_page_load)
        #self.camera_recognition_page.setVisible(False)
        #stacked_widget.addWidget(video_recognition_page)
        #stacked_widget.addWidget(usage_record_page)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.stacked_widget, '功能')  #当前页面
        #self.tab_widget.addTab(QTextEdit(), '帮助')
        #用户下拉菜单
        drop_down_menu=UserDropDown()
        #返回主页面
        return_to_home=Return_to_home()
        # 创建布局管理器




        self.icon_label = QLabel(self)

        self.icon_label.setPixmap(QPixmap("./avatar5.jpg"))  # 设置图标图片路径
        self.icon_label.setFixedSize(50, 50)  # 设置图标大小
        self.icon_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.icon_label.setScaledContents(True)  # 图片按比例缩放
        # 设置标签位置和点击事件
        self.icon_label.move(10, 10)  # 设置图标位置
        self.icon_label.mousePressEvent = self.return_to_home  # 绑定点击事件

        nav_layout = QHBoxLayout()
        #nav_layout.addWidget(return_to_home)
        nav_layout.addWidget(self.icon_label)
        nav_layout.addWidget(face_recognition_btn)
        nav_layout.addWidget(camera_recognition_btn)
        nav_layout.addWidget(video_recognition_btn)
        nav_layout.addWidget(usage_record_btn)
        nav_layout.addWidget(drop_down_menu)
        #nav_layout.addWidget(tab_widget)
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.tab_widget)


        # 设置布局管理器
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        face_recognition_btn.clicked.connect(self.add_and_show_picture)
        camera_recognition_btn.clicked.connect(self.add_and_show_camera)
        video_recognition_btn.clicked.connect(self.add_and_show_video_uplaoad)
        usage_record_btn.clicked.connect(self.add_and_show_record)

        self.stacked_widget.currentChanged.connect(self.switch_page)  #检测页面切换
        self.stacked_widget.blockSignals(True)   #信号锁
        qbtn=QPushButton('进行人脸表情识别')
        #self.video_recognition_page_load = Videoupload(self.model)
        self.video_recognition_page_load.vbox.addWidget(qbtn)
        qbtn.clicked.connect(self.add_and_show_video_run)
        qbtn.clicked.connect(self.switch_video_run)
        # 信号槽连接
        #face_recognition_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(face_recognition_page))
        #camera_recognition_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(camera_recognition_page))
        #video_recognition_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(video_recognition_page))
        #usage_record_btn.clicked.connect(lambda: stacked_widget.setCurrentWidget(usage_record_page))
    def return_to_home(self, event):
        # 处理点击事件，这里是返回主页的操作
        print("返回主页")
    def switch_page(self,page_name):    #每当页面切换时，添加相机表情识别记录
        self.stacked_widget.blockSignals(True) 
        #current=self.stacked_widget.currentIndex()
        #print(str(current)+'fff')
        self.end_time=time.time()
        
        runtime=self.end_time-self.start_time
        print(self.end_time)
        runtime=int(runtime)
        print(runtime)
        url='http://127.0.0.1:5000/add_camera_record/'
        data={'number':self.number,'usagetime':runtime}
        response = requests.post(url, json=data)
        
    #摄像头  
    def add_and_show_camera(self):
        current_widget_index = self.stacked_widget.currentIndex()
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        #self.camera_recognition_page = Camera(self.model)
        #self.capture=self.camera_recognition_page.capture
        self.start_time=time.time()
        print(self.start_time)
        if(self.stacked_widget.indexOf(self.camera_recognition_page)==-1): 
            self.camera_recognition_page=Camera(self.model)
            self.stacked_widget.addWidget(self.camera_recognition_page)
        self.camera_recognition_page.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.camera_recognition_page)
        self.stacked_widget.blockSignals(False)  #信号锁
        current_widget_index = self.stacked_widget.currentIndex()
        
    #图片
    def add_and_show_picture(self):
        current_widget_index = self.stacked_widget.currentIndex()
        #print(str(current_widget_index)+'ggg')  
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.currentWidget().setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        #self.face_recognition_page = Picture(self.model,self.number)
        if(self.stacked_widget.indexOf(self.face_recognition_page)==-1):   
            self.stacked_widget.addWidget(self.face_recognition_page)
        self.face_recognition_page.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.face_recognition_page)
        #print(str(current_widget_index)+'aaaa')
        current_widget_index = self.stacked_widget.currentIndex()
    #视频上传

    def add_and_show_video_uplaoad(self):
        current_widget_index = self.stacked_widget.currentIndex()
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        self.filename=self.video_recognition_page_load.video_path
        if(self.stacked_widget.indexOf(self.video_recognition_page_load)==-1):   
            self.stacked_widget.addWidget(self.video_recognition_page_load)
        self.video_recognition_page_load.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.video_recognition_page_load)
        current_widget_index = self.stacked_widget.currentIndex()
        
    #视频表情识别
    def add_and_show_video_run(self):
        
        current_widget_index = self.stacked_widget.currentIndex()
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        self.filename=self.video_recognition_page_load.video_path
        if(self.stacked_widget.indexOf(self.video_recognition_page)==-1):
            self.video_recognition_page = Camera(self.model,self.filename)
            qbtn=QPushButton('返回重新上传')
            self.video_recognition_page.hbox.addWidget(qbtn)
            qbtn.clicked.connect(self.add_and_show_video_uplaoad)
            qbtn.clicked.connect(self.switch_video_upload)   
            self.stacked_widget.addWidget(self.video_recognition_page)
        self.video_recognition_page.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.video_recognition_page)
        current_widget_index = self.stacked_widget.currentIndex()

    @pyqtSlot()
    def switch_video_run(self):
        self.start_time=time.time()
        #print('switch_video_run')
    @pyqtSlot()
    def switch_video_upload(self):
        self.end_time=time.time()
        runtime=self.end_time-self.start_time
        #print(runtime)
        runtime=int(runtime)
        url='http://127.0.0.1:5000/add_video_record/'
        data={'number':self.number,'usagetime':runtime}
        response = requests.post(url, json=data)
        #print("switch_video_upload")


    def add_and_show_record(self):
        current_widget_index = self.stacked_widget.currentIndex()
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        #self.usage_record_page = UsageRecord()
        #qbtn=QPushButton('tbn')
        #self.usage_record_page.vbox.addWidget(qbtn)
        if(self.stacked_widget.indexOf(self.usage_record_page)==-1):   
            self.stacked_widget.addWidget(self.usage_record_page)
        self.usage_record_page.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.usage_record_page)
        current_widget_index = self.stacked_widget.currentIndex()
        #print(current_widget_index)        

  



if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    model=load_model()
    windowMain= MainWindow(model)
    #window2.show()
    windowLogin=LoginWindow(windowMain)
    windowRegister=RegisterWindow(windowLogin)
    windowLogin.show()
    sys.exit(app.exec_())
  