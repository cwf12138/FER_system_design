import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
#from my_module import my_function  # 导入需要调用的Python函数
from recognition_camera import predict_expression

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个按钮和一个标签
        self.button = QPushButton("Click me")
        self.label = QLabel("")

        # 设置标签的对齐方式和最小高度
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumHeight(50)

        # 创建一个垂直布局，并将按钮和标签添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        # 将布局设置为窗口的主布局
        self.setLayout(layout)

        # 连接按钮的点击事件到槽函数
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # 当按钮被点击时，调用指定的Python函数，并在标签中显示返回值
        result = predict_expression()
        self.label.setText(result)


if __name__ == '__main__':
    # 创建PyQt5应用程序对象
    app = QApplication(sys.argv)

    # 创建窗口对象并显示
    window = MyWindow()
    window.show()

    # 运行应用程序并等待退出
    sys.exit(app.exec_())
