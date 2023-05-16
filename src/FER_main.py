import sys,cv2,time,requests,os
from PyQt5.QtCore import Qt,pyqtSlot,pyqtSignal,QThread
from PyQt5.QtGui import QPixmap,QIcon,QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import  QLineEdit, QTextEdit, QStackedWidget, QTabWidget,QMainWindow,QFrame,QMenu,QAction
from qt_material import apply_stylesheet
from recognition_camera import Camera,load_model
from recognition_picture import Picture
from recognition_record import Camera_table,Video_table,Picture_table
from qtupload import Videoupload
from your_profile import UserDropDown
from return_to_home import Return_to_home
#from login_and_register import LoginWindow,RegisterWindow
from user_profile import UserProfile
from getdata import get_picture_usage_record,get_camera_usage_record,get_video_usage_record,get_user_profile
sys.path.append('../')
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
        




#Qwidget
class Return_to_homepage(QWidget):  #主页，欢迎页，但感觉有一点单调了
    def __init__(self,name):
        super().__init__()
        self.name=name
        self.initUI()
    def initUI(self):
        welcome_label=QLabel("欢迎使用人脸表情识别系统")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.label = QLabel(f"尊敬的{self.name}用户!",self)
        #label.setGeometry(100, 80, 200, 40)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        vbox=QVBoxLayout()
        vbox.addWidget(welcome_label)
        vbox.addWidget(self.label)
        self.setLayout(vbox)

class AvatarThread(QThread):
    resultChanged = pyqtSignal(bool)

    def __init__(self, param1, param2, parent=None):
        super().__init__(parent)
        self.param1 = param1
        self.param2 = param2

    def run(self):
        while True:
            # 在这里实时判断参数是否相等
            if self.param1 != self.param2:
                self.resultChanged.emit(False)
            else:
                self.resultChanged.emit(True)
            self.sleep(1)  # 休眠一秒钟再进行下一次判断



#Qwidget
class MainWindow(QMainWindow):
    def __init__(self,model,number,window):
        super().__init__()
        self.model=model
        self.filename=''
        self.number=number
        self.window=window
        self.initUI()
        


    def initUI(self):
        # 添加组件
        self.resize(1000,800)
        self.setWindowIcon(QIcon("./avatar.jpg"))  # 设置窗口图标
        #self.setWindowIcon(QIcon())  #设置窗口图标为空
        self.setWindowTitle(" ")
        #self.setWindowFlags(Qt.FramelessWindowHint)
        main_widget=QWidget()
        title_label = QLabel('人脸表情识别系统')
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        #获取用户信息
        profile=get_user_profile(self.number)
        print(profile['avatar'])
        print(profile['name'])
        self.avatar=profile['avatar']
        self.name=profile['name']


        face_recognition_btn = QPushButton('基于图片的表情识别')
        camera_recognition_btn = QPushButton('基于摄像头的表情识别')
        video_recognition_btn = QPushButton('基于视频的表情识别')
        usage_record_btn = QPushButton('查看使用记录')
        # 创建堆叠窗口和页面
        self.stacked_widget = QStackedWidget()
        #主页面
        self.homepage=Return_to_homepage(self.name)
        #图片表情识别
        self.face_recognition_page = Picture(self.model,self.number)
        #个人资料界面
        self.userprofile_page=UserProfile(self.name,self.avatar,self.number)
        self.userprofile_page.avatar_changed.connect(self.handle_property_changed)  #实时监测其他页面中的属性变化
        self.userprofile_page.name_changed.connect(self.changed_name)
        #self.camera_recognition_page = Camera(self.model)
        #摄像头表情识别
        self.camera_recognition_page=QWidget()
        self.camera_recognition_page.setVisible(False)
        #视频上传界面
        self.video_recognition_page_load = Videoupload(self.model)
        #camera_recognition_page = Camera(self.model)
        #self.video_recognition_page = VideoRecognition(self.model)
        #视频表情识别
        self.video_recognition_page=QWidget()
        self.usage_record_page = UsageRecord(self.number)
        #添加到堆叠窗口里
        self.stacked_widget.addWidget(self.homepage)
        self.stacked_widget.addWidget(self.face_recognition_page)
        self.stacked_widget.addWidget(self.usage_record_page)
        #self.stacked_widget.addWidget(self.camera_recognition_page)
        self.stacked_widget.addWidget(self.video_recognition_page_load)
        self.stacked_widget.addWidget(self.userprofile_page)
        
        #self.camera_recognition_page.setVisible(False)
        #stacked_widget.addWidget(video_recognition_page)
        #stacked_widget.addWidget(usage_record_page)

        #*创建标签页  重要
        #self.tab_widget = QTabWidget()
        #self.tab_widget.addTab(self.stacked_widget,' ')  #当前页面
        #self.tab_widget.addTab(QTextEdit(), '帮助')



        #用户下拉菜单
        self.button = QPushButton()
        self.button.setFixedSize(40, 40)
        icon=QIcon(self.avatar)
        #icon = QIcon("C:/Users/cwf/FacialExpressionRecognition/avatar2.jpg")  # 替换为您自己的图标路径
        pixmap = icon.pixmap(40, 40)  # 调整图标大小为 40x40 像素
        #self.button.setIcon(QIcon('./avatar2.jpg'))
        self.button.setIcon(QIcon(pixmap))
        self.button.setIconSize(self.button.size())
        #font = self.button.font()
        #font.setPointSize(50)  # 设置字体大小为20
        #self.button.setFont(font)
        #self.button.setIconSize(Qt.Size(24, 24))
        self.button.setStyleSheet("QPushButton {border: none;}")

        # 创建一个下拉菜单
        self.menu = QMenu(self)
        self.menu.setStyleSheet("QMenu {background-color: white; border: 1px solid gray;}")
        self.menu.setFixedWidth(200)

        # 添加菜单项
        #self.menu.addAction('你的个人资料')
        action1=QAction('你的个人资料',self)
        action1.triggered.connect(self.open_userprofile)
        self.menu.addAction(action1)

        #self.menu.addAction('设置')
        #self.menu.addAction('退出')
        action2=QAction('退出',self)
        action2.triggered.connect(self.return_to_login)
        self.menu.addAction(action2)
        #self.menu.addAction('Your profile')
        #self.menu.addAction('Settings')
        #self.menu.addAction('Sign out')
        # 将菜单添加到按钮中
        self.button.setMenu(self.menu)



        #用户下拉菜单
        drop_down_menu=UserDropDown()
        #返回主页面
        return_to_home=Return_to_home()
        # 创建布局管理器

        #左上角返回主页标签 
        self.icon_label = QLabel(self)

        self.icon_label.setPixmap(QPixmap("./avatar.jpg"))  # 设置图标图片路径
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
        #nav_layout.addWidget(drop_down_menu)
        nav_layout.addWidget(self.button)
        #nav_layout.addWidget(tab_widget)
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(nav_layout)
        #分割线
        separator_line_h = QFrame()   #separator_line_h.setLineWidth(3)#separator_line_h.setMidLineWidth(3) 增加宽度
        separator_line_h.setFrameShape(QFrame.HLine)
        separator_line_h.setFrameShadow(QFrame.Sunken)
        # separator_line_hf = QFrame()   #separator_line_h.setLineWidth(3)#separator_line_h.setMidLineWidth(3) 增加宽度
        # separator_line_hf.setFrameShape(QFrame.HLine)
        # separator_line_hf.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator_line_h)
        #main_layout.addWidget(separator_line_hf)
        #main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.stacked_widget)
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

    #信号槽机制   -----实时监测其他页面中的属性变化  
    def changed_name(self,new_value):
        self.name=new_value
        self.homepage.label.setText(f"尊敬的{self.name}用户!")
        print(new_value)
        #self.label = QLabel(f"尊敬的{self.name}用户!",self)
        
    def handle_property_changed(self, new_value):
        # 执行属性变化后的操作
        self.avatar=new_value
        icon=QIcon(self.avatar)
        #icon = QIcon("C:/Users/cwf/FacialExpressionRecognition/avatar2.jpg")  # 替换为您自己的图标路径
        pixmap = icon.pixmap(40, 40)  # 调整图标大小为 40x40 像素
        #self.button.setIcon(QIcon('./avatar2.jpg'))
        self.button.setIcon(QIcon(pixmap))
        self.button.setIconSize(self.button.size())

        print("Property changed:", new_value)
    def return_to_login(self):
        self.close()
        self.window.show()
    def open_userprofile(self):
        current_widget_index = self.stacked_widget.currentIndex()
        #print(str(current_widget_index)+'ggg')  
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.currentWidget().setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        #self.face_recognition_page = Picture(self.model,self.number)
        if(self.stacked_widget.indexOf(self.userprofile_page)==-1):   
            self.stacked_widget.addWidget(self.userprofile_page)
        self.userprofile_page.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.userprofile_page)
        self.avatar=self.userprofile_page.avatar
        #print(str(current_widget_index)+'aaaa')
        #current_widget_index = self.stacked_widget.currentIndex()
        #print('xx')
    def return_to_home(self, event):
        # 处理点击事件，这里是返回主页的操作
        current_widget_index = self.stacked_widget.currentIndex()
        #print(str(current_widget_index)+'ggg')  
        widget_to_remove = self.stacked_widget.widget(current_widget_index)
        widget_to_remove.setVisible(False)
        #self.stacked_widget.currentWidget().setVisible(False)
        #self.stacked_widget.removeWidget(widget_to_remove)  
        #widget_to_remove.deleteLater()
        #self.face_recognition_page = Picture(self.model,self.number)
        if(self.stacked_widget.indexOf(self.homepage)==-1):   
            self.stacked_widget.addWidget(self.homepage)
        self.homepage.setVisible(True)
        self.stacked_widget.setCurrentWidget(self.homepage)
        #print(str(current_widget_index)+'aaaa')
        current_widget_index = self.stacked_widget.currentIndex()
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
    number='18212139396'
    windowMain= MainWindow(model,number)
    windowMain.show()
    #window2.show()
    # windowLogin=LoginWindow(windowMain)
    # windowRegister=RegisterWindow(windowLogin)
    # windowLogin.show()
    sys.exit(app.exec_())
  



