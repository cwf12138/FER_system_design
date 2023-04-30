import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建堆栈容器
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 创建页面1
        self.page1 = QWidget()
        layout1 = QVBoxLayout(self.page1)
        button1 = QPushButton("切换到页面2")
        button1.clicked.connect(self.show_page2)
        layout1.addWidget(button1)

        # 创建页面2
        self.page2 = QWidget()
        layout2 = QVBoxLayout(self.page2)
        button2 = QPushButton("切换到页面1")
        button2.clicked.connect(self.show_page1)
        layout2.addWidget(button2)

        # 将页面添加到堆栈容器中
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

    def show_page1(self):
        # 切换到页面1
        self.stacked_widget.setCurrentWidget(self.page1)

    def show_page2(self):
        # 切换到页面2
        self.stacked_widget.setCurrentWidget(self.page2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
