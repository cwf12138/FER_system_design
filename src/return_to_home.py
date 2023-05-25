from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication
from qt_material import apply_stylesheet       #这个文件部分也是暂时没有用      
class Return_to_home(QWidget):
    def __init__(self):
        super().__init__()
        #self.setWindowTitle("窗口图标示例")
        #self.setGeometry(100, 100, 400, 300)
        # 创建图标标签
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap("./avatar3.jpg"))  # 设置图标图片路径
        self.icon_label.setFixedSize(40, 40)  # 设置图标大小
        self.icon_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.icon_label.setScaledContents(True)  # 图片按比例缩放
        
        # 设置标签位置和点击事件
        self.icon_label.move(10, 10)  # 设置图标位置
        self.icon_label.mousePressEvent = self.return_to_home  # 绑定点击事件
        
    def return_to_home(self, event):
        # 处理点击事件，这里是返回主页的操作
        print("返回主页")
        # 添加你返回主页的具体代码逻辑
    
class Label(QLabel):

    def __init__(self, *args, antialiasing=True, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.Antialiasing = antialiasing
        #self.setMaximumSize(200, 200)
        #self.setMinimumSize(200, 200)
        self.radius = 100
        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明

        p = QPixmap("./photo1.jpg").scaled(  # 加载图片并缩放和控件一样大
            200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            # 抗锯齿
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        #         painter.setPen(# 测试圆圈
        #             QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.width(), self.height(), self.radius, self.radius)
        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        #         painter.drawPath(path)  # 测试圆圈

        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)
        #####################核心实现#########################



if __name__ == "__main__":
    app = QApplication([])
    window = Return_to_home()
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    window.show()
    app.exec_()
