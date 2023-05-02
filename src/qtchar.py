from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication([])
window = QMainWindow()

# 创建数据集
data = [1, 2, 3, 4, 5]
bar_set = QBarSet('数据集')
for value in data:
    bar_set.append(value)

# 创建条形图系列
bar_series = QBarSeries()
bar_series.append(bar_set)

# 创建图表并添加系列
chart = QChart()
chart.addSeries(bar_series)

# 设置图表的标题和横坐标标签
chart.setTitle('条形图')
chart.setAnimationOptions(QChart.SeriesAnimations)
chart.createDefaultAxes()
chart.axisX().setTitleText('横坐标')
chart.axisY().setTitleText('纵坐标')

# 创建图表视图并设置图表视图为主窗口的中心部分
chart_view = QChartView(chart)
window.setCentralWidget(chart_view)
window.show()

app.exec_()
