from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QLineEdit,QFormLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize

from qt_material import apply_stylesheet
class MainWindow(QWidget):
    def __init__(self,name):
        super().__init__()
        self.name=name

        # 设置窗口标题
        self.setWindowTitle("User Profile")

        # 创建布局
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # 左半部分布局
        avatar_label = QLabel(self)
        avatar_label.setFixedSize(300, 300)
        avatar_label.setScaledContents(True)
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setStyleSheet("""
            border: 2px solid #ccc;
            border-radius: 50px;
        """)
        avatar_label.mousePressEvent = self.change_avatar

        avatar_image = QImage("./photo1.jpg")
        avatar_pixmap = QPixmap.fromImage(avatar_image)
        avatar_label.setPixmap(avatar_pixmap)

        username_label = QLabel("John Doe", self)
        username_label.setAlignment(Qt.AlignCenter)
        username_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        left_layout.addWidget(avatar_label)
        left_layout.addWidget(username_label)
        left_layout.addStretch()

        # 右半部分布局
        #修改用户名
        self.text_username=QLineEdit()
        self.text_username.setStyleSheet("font-size: 20px;")
        self.text_username.setPlaceholderText(self.name)  # 设置提示文本
        btn_modifyusername=QPushButton('修改用户名')
        btn_modifyusername.clicked.connect(self.modify_username)

        #修改密码
        label_password=QLabel("修改密码")
        label_password.setStyleSheet("font-size: 18px; font-weight: bold;")
        old_password=QLabel("旧密码")
        self.old_password=QLineEdit()
        self.old_password.setEchoMode(QLineEdit.Password)
        new_password=QLabel("新密码")
        self.new_password=QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        confirm_new_password=QLabel("确认新密码")
        self.confirm_new_password=QLineEdit()
        self.confirm_new_password.setEchoMode(QLineEdit.Password)
        btn_update_password=QPushButton("更新密码")
        btn_update_password.clicked.connect(self.update_password)
        
        # 将布局添加到主布局中
        #right_layout.setSpacing(0)
        update_username=QFormLayout()
        update_username.addRow(self.text_username)
        update_username.addRow(btn_modifyusername)
        #right_layout.addWidget(self.text_username)
        #right_layout.addWidget(btn_modifyusername)
        right_layout.addLayout(update_username)

        #right_layout.addWidget(label_passowrd)
        update_password=QFormLayout()
        update_password.addRow(label_password)
        update_password.addRow(old_password)
        update_password.addRow(self.old_password)
        update_password.addRow(new_password)
        update_username.setSpacing(20)
        update_password.addRow(self.new_password)
        update_password.addRow(confirm_new_password)
        update_password.addRow(self.confirm_new_password)
        update_password.addRow(btn_update_password)
        right_layout.addLayout(update_password)

        # right_layout.addWidget(old_password)
        # right_layout.addWidget(self.old_password)
        # right_layout.addWidget(new_password)
        
        # right_layout.addWidget(self.new_password)
        # right_layout.addWidget(confirm_new_password)
        # right_layout.addWidget(self.confirm_new_password)
        # right_layout.addWidget(btn_update_password)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def change_avatar(self, event):
        # 处理头像点击事件，实现头像更换逻辑
        print("Change Avatar")
    def modify_username(self):
        print(self.text_username.text())
    def update_password(self):
        print(self.new_password.text())

if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    window = MainWindow('cwf')
    window.show()
    app.exec_()
