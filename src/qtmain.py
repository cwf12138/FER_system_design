import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from qtupload import MainWindow,load_model
from recognition_camera import Camera
from qt_material import apply_stylesheet
from qt_material import list_themes
class Window(QMainWindow):
    def __init__(self,model):
        super().__init__()

        # 创建堆栈容器
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.model=model
        # 创建页面1
        self.page1=MainWindow(self.model)  #print(self.page1) #print(type(self.page1)) #layout1 = QVBoxLayout(self.page1)
        button1 = QPushButton("切换到页面2")
        button1.clicked.connect(self.show_page2)  #layout1.addWidget(button1) #layout1=self.page1.layout
        layout1=self.page1.vbox
        layout1.addWidget(button1)
        self.filename=self.page1.video_path

        # 创建页面1
        self.stacked_widget.addWidget(self.page1)
        #self.stacked_widget.addWidget(self.page2)

    def show_page2(self):
        # 切换到页面1
        #self.stacked_widget.setCurrentWidget(self.page1)
        self.filename=self.page1.video_path
        #print(self.filename) 
        self.page2 = Camera(model,self.filename)
        layout2=self.page2.vbox
        #layout2 = QVBoxLayout(self.page2)
        button2 = QPushButton("切换到页面1")
        button2.clicked.connect(self.show_page1)
        layout2.addWidget(button2)
        #判断当前Qwidget是否在stacked_widget里面
        if(self.stacked_widget.indexOf(self.page2)==-1):   
            self.stacked_widget.addWidget(self.page2)
        #self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.setCurrentWidget(self.page2)
        current_widget_index = self.stacked_widget.currentIndex()
        print(current_widget_index)

    def show_page1(self):
        # 切换到页面2
        #self.stacked_widget.setCurrentWidget(self.page1)
        current_widget_index = self.stacked_widget.currentIndex()  
        widget_to_remove = self.stacked_widget.widget(current_widget_index) 
        self.stacked_widget.removeWidget(widget_to_remove) 
        widget_to_remove.deleteLater()  #最后，使用 deleteLater() 方法释放 QWidget 的内存。
        self.stacked_widget.setCurrentWidget(self.page1)
        current_widget_index = self.stacked_widget.currentIndex()
        print(current_widget_index)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #apply_stylesheet(app, theme='dark_teal.xml')
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    #print(list_themes())
    model=load_model()
    window = Window(model)
    window.show()
    sys.exit(app.exec_())
