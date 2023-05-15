from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QLineEdit,QFormLayout,QFrame,QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import requests,json
from qt_material import apply_stylesheet
class UserProfile(QWidget):
    avatar_changed = pyqtSignal(str)
    def __init__(self,name,avatar,number):
        super().__init__()
        self.name=name
        self.avatar=avatar
        self.number=number

        # 设置窗口标题
        self.setWindowTitle("User Profile")

        # 创建布局
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 左半部分布局
        self.avatar_label = QLabel(self)     #头像
        self.avatar_label.setFixedSize(300, 300)
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("""
            border: 2px solid #ccc;
            border-radius: 50px;
        """)
        self.avatar_label.mousePressEvent = self.change_avatar  
        #头像地址
        avatar_image = QImage(self.avatar)   
        avatar_pixmap = QPixmap.fromImage(avatar_image)
        self.avatar_label.setPixmap(avatar_pixmap)
        #头像下方的用户名
        self.username_label = QLabel(self.name, self)
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setStyleSheet("font-size: 23px; font-weight: bold;")

        left_layout.addWidget(self.avatar_label)
        left_layout.addWidget(self.username_label)
        left_layout.addStretch()

        # 右半部分布局
        #修改用户名
        label_username=QLabel("修改用户名")
        label_username.setStyleSheet("font-size: 23px; font-weight: bold;")
        self.text_username=QLineEdit()
        self.text_username.setStyleSheet("font-size: 25px;")
        self.text_username.setPlaceholderText(self.name)  # 设置提示文本
        btn_modifyusername=QPushButton('更新用户名')
        btn_modifyusername.clicked.connect(self.modify_username)

        #水平分割线
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        #修改密码
        label_password=QLabel("修改密码")
        label_password.setStyleSheet("font-size: 23px; font-weight: bold;") #修改字体样式
        
        old_password=QLabel("旧密码")
        old_password.setStyleSheet("font-size :18px;")
        self.old_password=QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)

        new_password=QLabel("新密码")
        new_password.setStyleSheet("font-size :18px;")
        self.new_password=QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)

        confirm_new_password=QLabel("确认新密码")
        confirm_new_password.setStyleSheet("font-size :18px;")
        self.confirm_new_password=QLineEdit()
        self.confirm_new_password.setEchoMode(QLineEdit.Password)

        btn_update_password=QPushButton("更新密码")
        btn_update_password.clicked.connect(self.update_password)
        #修改密码提示信息
        self.lbl_message = QLabel(self)
        self.lbl_message.setAlignment(Qt.AlignCenter)
        self.lbl_message.setStyleSheet("font-size: 18px;")
        #right_layout.setSpacing(0)
        #使用Qfromlayout可以使得每一个表情距离变近，距离更小
        update_username=QFormLayout()       
        update_username.addRow(label_username)    #修改用户名部分
        update_username.addRow(self.text_username)
        update_username.addRow(btn_modifyusername)
        right_layout.addLayout(update_username)

        #right_layout.addWidget(label_passowrd)
        update_password=QFormLayout()
        update_password.addRow(label_password)     #修改密码部分
        update_password.addRow(self.line2)
        update_password.addRow(old_password)
        update_password.addRow(self.old_password)
        update_password.addRow(new_password)
        update_password.addRow(self.new_password)
        update_password.addRow(confirm_new_password)
        update_password.addRow(self.confirm_new_password)
        update_password.addRow(btn_update_password)
        right_layout.addLayout(update_password)
        right_layout.addWidget(self.lbl_message)

         # 将布局添加到主布局中
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
    def update_avatar(self, new_value):
        if self.avatar != new_value:
            self.avatar = new_value
            self.avatar_changed.emit(self.avatar)
    def change_avatar(self, event):
        # 处理头像点击事件，实现头像更换逻辑
        file_name, file_type = QFileDialog.getOpenFileName(caption="选取图片", directory="./input/test/",
                                                                     filter="All Files (*);;Text Files (*.txt)")
        if file_name is not None and file_name != "":
            #self.avatar=file_name
            self.update_avatar(file_name)
            url="http://127.0.0.1:5000/modify_avatar/"
            data={'number':self.number,'avatar':self.avatar}
            response = requests.post(url,json=data)
            datas=json.loads(response.content.decode('utf-8'))
            avatar_image = QImage(self.avatar)   
            avatar_pixmap = QPixmap.fromImage(avatar_image)
            self.avatar_label.setPixmap(avatar_pixmap)


        #print("Change Avatar")
    def modify_username(self):
        name=self.text_username.text()
        data={'number':self.number,'name':name}
        url="http://127.0.0.1:5000/modify_name/"
        response = requests.post(url,json=data)
        datas=json.loads(response.content.decode('utf-8'))
        self.name=name
        self.username_label.setText(self.name)
        self.text_username.setPlaceholderText(self.name)  # 设置提示文本
        #print(self.text_username.text())
    def update_password(self):
        get_old_password=self.old_password.text()
        get_new_password=self.new_password.text()
        get_confirm_new_password=self.confirm_new_password.text()
        self.msg=""
        if get_new_password==get_confirm_new_password:
            url="http://127.0.0.1:5000/modify_password/"
            data={'number':self.number,'oldpassword':get_old_password,'newpassword':get_new_password}
            response = requests.post(url,json=data)
            datas=json.loads(response.content.decode('utf-8'))
            self.msg=datas['msg']
        else:
            self.msg="两次的新密码输入不一致"
        self.lbl_message.setText(self.msg)



        print(self.new_password.text())

if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    name='cwf'
    avatar='C:/Users/cwf/FacialExpressionRecognition/input/test/Pinterest_Download.jpg'
    number='18212139396'
    window = UserProfile(name,avatar,number)
    window.show()
    app.exec_()
