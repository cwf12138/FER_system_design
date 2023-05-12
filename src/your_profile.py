from PyQt5.QtWidgets import QApplication, QMenu, QMenuBar, QAction, QToolBar, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt,QFile,QTextStream
from qt_material import apply_stylesheet
class UserDropDown(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 创建一个按钮
        self.button = QPushButton()
        self.button.setFixedSize(30, 30)
        
        self.button.setIcon(QIcon('./avatar2.jpg'))
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
        self.menu.addAction('你的个人资料')
        #self.menu.addAction('设置')
        self.menu.addAction('退出')
        #self.menu.addAction('Your profile')
        #self.menu.addAction('Settings')
        #self.menu.addAction('Sign out')
        # 将菜单添加到按钮中
        self.button.setMenu(self.menu)

        # 创建一个布局，并将按钮添加到布局中
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    style_file = QFile("./style.css")
    if style_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(style_file)
        app.setStyleSheet(stream.readAll())
        style_file.close()
    ex = UserDropDown()
    ex.show()
    sys.exit(app.exec_())
