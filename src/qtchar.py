from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter

class BarChart(QMainWindow):
    def __init__(self, x, y):
        super().__init__()

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
        
        # 将图表视图设置为主窗口的中央部件
        self.setCentralWidget(chartView)


if __name__ == "__main__":
    x = ['anger', 'disgust', 'fear', 'happy', 'sad', 'surprised', 'neutral', 'contempt']
    y = [10, 5, 7, 15, 3, 8, 20, 2]
    app = QApplication([])
    window = BarChart(x, y)
    window.show()
    app.exec_()
