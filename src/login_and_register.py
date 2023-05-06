from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon,QPixmap
from PyQt5.QtCore import Qt
import requests,json
from qt_material import apply_stylesheet
class LoginWindow(QWidget):
    def __init__(self,window):
        super().__init__()
        #self.setWindowTitle("Login")
        self.window=window
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon("./avatar.jpg"))  # 设置窗口图标
        self.setStyleSheet("background-color: #f6f8fa;")  # 设置窗口背景色
        self.msg=''
        self.flag=''
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # GitHub icon
        icon_label = QLabel(self)
        icon_label.setPixmap(QPixmap("./avatar.jpg").scaled(64, 64))  # 设置图标大小
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Title label
        #title_label = QLabel("Sign in to GitHub", self)
        title_label = QLabel("登录", self)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username input
        #lbl_username = QLabel("Username or email address", self)
        lbl_username = QLabel("账号", self)
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("手机号")  # 设置提示文本
        layout.addWidget(lbl_username)
        layout.addWidget(self.txt_username)

        # Password input
        #lbl_password = QLabel("Password", self)
        lbl_password = QLabel("密码", self)
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(lbl_password)
        layout.addWidget(self.txt_password)

        # Sign in button
        #btn_signin = QPushButton("Sign in", self)
        btn_signin = QPushButton("登录", self)
        btn_signin.clicked.connect(self.sign_in)
        layout.addWidget(btn_signin)

        # Forgot password link
        forgot_password_label = QLabel('<a href="#">Forgot password?</a>', self)
        forgot_password_label.setAlignment(Qt.AlignRight)
        layout.addWidget(forgot_password_label)
        # Create account link
        create_account_label = QLabel('<a href="#">Create an account</a>', self)
        create_account_label.setAlignment(Qt.AlignRight)
        layout.addWidget(create_account_label)
        #登录提示信息
        self.lbl_message = QLabel(self)
        self.lbl_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_message)
        # Horizontal layout for links
        links_layout = QHBoxLayout()
        links_layout.addWidget(forgot_password_label)
        links_layout.addWidget(create_account_label)
        layout.addLayout(links_layout)

        self.setLayout(layout)

    def sign_in(self):

        number = self.txt_username.text()
        password = self.txt_password.text()
        
        # Perform sign in authentication here
        # You can use the entered username and password for authentication
        data={'number':number,'password':password}
        url="http://127.0.0.1:5000/login/"
        response = requests.post(url,json=data)
        datas=json.loads(response.content.decode('utf-8'))
        self.msg=datas['msg']
        self.flag=datas['flag']
        self.lbl_message.setText(self.msg)
        print(self.msg)
        print(self.flag)
        if self.flag=='1':
            self.hide()
            self.window.show()


class RegisterWindow(QWidget):
    def __init__(self,window):
        super().__init__()
        #self.setWindowTitle("Login")
        self.window=window
        self.setWindowTitle("注册账户")
        self.setWindowIcon(QIcon("./avatar.jpg"))  # 设置窗口图标
        self.setStyleSheet("background-color: #f6f8fa;")  # 设置窗口背景色
        self.msg=''
        self.flag=''
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # GitHub icon
        icon_label = QLabel(self)
        icon_label.setPixmap(QPixmap("./avatar.jpg").scaled(64, 64))  # 设置图标大小
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Title label
        #title_label = QLabel("Sign in to GitHub", self)
        title_label = QLabel("注册", self)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)


        lbl_username = QLabel("用户名", self)
        self.txt_username = QLineEdit()
        #self.txt_username.setPlaceholderText("手机号")  # 设置提示文本
        layout.addWidget(lbl_username)
        layout.addWidget(self.txt_username)

        # Username input
        #lbl_username = QLabel("Username or email address", self)
        lbl_number = QLabel("账号", self)
        self.txt_number = QLineEdit()
        self.txt_number.setPlaceholderText("手机号")  # 设置提示文本
        layout.addWidget(lbl_number)
        layout.addWidget(self.txt_number)

        # Password input
        #lbl_password = QLabel("Password", self)
        lbl_password = QLabel("密码", self)
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_username.setPlaceholderText("最少6位数")  # 设置提示文本
        layout.addWidget(lbl_password)
        layout.addWidget(self.txt_password)

        # Sign in button
        #btn_signin = QPushButton("Sign in", self)
        btn_signin = QPushButton("登录", self)
        btn_signin.clicked.connect(self.sign_in)
        layout.addWidget(btn_signin)

        # Forgot password link
        forgot_password_label = QLabel('<a href="#">Forgot password?</a>', self)
        forgot_password_label.setAlignment(Qt.AlignRight)
        layout.addWidget(forgot_password_label)
        # Create account link
        create_account_label = QLabel('<a href="#">Create an account</a>', self)
        create_account_label.setAlignment(Qt.AlignRight)
        layout.addWidget(create_account_label)
        #登录提示信息
        self.lbl_message = QLabel(self)
        self.lbl_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_message)
        # Horizontal layout for links
        links_layout = QHBoxLayout()
        links_layout.addWidget(forgot_password_label)
        links_layout.addWidget(create_account_label)
        layout.addLayout(links_layout)

        self.setLayout(layout)

    def sign_in(self):
        username=self.txt_username.text()
        number = self.txt_number.text()
        password = self.txt_password.text()
        
        # Perform sign in authentication here
        # You can use the entered username and password for authentication
        data={'number':number,'password':password,'username':username}
        url="http://127.0.0.1:5000/register/"
        response = requests.post(url,json=data)
        datas=json.loads(response.content.decode('utf-8'))
        self.msg=datas['msg']
        self.flag=datas['flag']
        self.lbl_message.setText(self.msg)
        print(self.msg)
        print(self.flag)
        if self.flag=='1':
            self.hide()
            self.window.show()


if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)

    app.exec()
