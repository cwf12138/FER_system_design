from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame,QSizePolicy
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt, QMargins,QRectF
from PyQt5.QtGui import QPainter,QFont,QColor
import random
class BarChart(QWidget):
    def __init__(self, x, y):
        super().__init__()
        #self.fff=y[0]
        # 创建条形集合并添加数据
        set0 = QBarSet("Quantity")
        for value in y:
            set0.append(value)

        # 将条形集合添加到条形系列中
        series = QBarSeries()
        series.append(set0)
        #series.setBarWidth(0.7)

        # 创建水平类别轴并设置类别
        axisX = QBarCategoryAxis()
        axisX.append(x)
        axisX.setLabelsFont(QFont("Arial", 8))
        #axisX.setLabelsAngle(-45)
        #axisX.setLabelsFont(QFont("Arial", 6))  # 设置较小的字体大小
        #axisX.setLabelsBrush(QColor("#000000"))  # 设置较小的颜色


        # 创建数值轴并设置范围
        axisY = QValueAxis()
        axisY.setRange(0, max(y)*1.2)

        # 将类别轴和数值轴添加到图表中
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Expression Distribution")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # 设置y轴坐标数值显示
        chart.axisY().setLabelFormat("%d")

        # 创建一个QFrame用于包裹图表视图
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        self.chartView=chartView
        # 将图表视图添加到QFrame中
        self.layout = QVBoxLayout(frame)
        self.layout.addWidget(self.chartView)
        #self.layout.addStretch()
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 将QFrame设置为主窗口的中央部件
        self.setLayout(self.layout)
    def update(self):
        # 随机生成柱状数据
        data = [random.randint(0, 10) for i in range(8)]
        for i in range(len(data)):
            self.bar_set.replace(i, data[i])    

if __name__ == "__main__":
    x = ['anger', 'disgust', 'fear', 'happy', 'sad', 'surprised', 'neutral', 'contempt']
    y = [10, 5, 7, 15, 3, 8, 20, 2]
    app = QApplication([])
    window = QMainWindow()
    widget = BarChart(x, y)
    window.setCentralWidget(widget)
    window.setMinimumSize(800, 400)
    
    window.show()
    app.exec_()
