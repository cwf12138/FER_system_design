from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame,QSizePolicy
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt, QMargins,QRectF
from PyQt5.QtGui import QPainter
class BarChart(QWidget):
    def __init__(self, x, y):
        super().__init__()
        self.fff=y[0]

        # 创建条形集合并添加数据
        set0 = QBarSet("Quantity")
        for value in y:
            set0.append(value)

        # 将条形集合添加到条形系列中
        series = QBarSeries()
        series.append(set0)

        # 创建水平类别轴并设置类别
        axisX = QBarCategoryAxis()
        axisX.append(x)

        # 创建数值轴并设置范围
        axisY = QValueAxis()
        axisY.setRange(0, max(y)*1.2)

        # 将类别轴和数值轴添加到图表中
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Emotion Distribution")
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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 将QFrame设置为主窗口的中央部件
        self.setLayout(self.layout)

if __name__ == "__main__":
    x = ['anger', 'disgust', 'fear', 'happy', 'sad', 'surprised', 'neutral', 'contempt']
    y = [10, 5, 7, 15, 3, 8, 20, 2]
    app = QApplication([])
    window = QMainWindow()
    widget = BarChart(x, y)
    window.setCentralWidget(widget)
    window.show()
    app.exec_()
