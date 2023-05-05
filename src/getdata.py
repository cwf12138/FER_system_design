import requests
import json
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QPushButton,QLabel
from PyQt5.QtCore import Qt
import random
from qt_material import apply_stylesheet




def get_picture_usage_record(number):
    url="http://127.0.0.1:5000/get_picture_record/"
    url=url+number
    response = requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas["datas"]
    return data

def get_video_usage_record(number):
    url="http://127.0.0.1:5000/get_video_record/"
    url=url+number
    response = requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas["datas"]
    return data

def get_camera_usage_record(number):
    url="http://127.0.0.1:5000/get_camera_record/"
    url=url+number
    response = requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas["datas"]
    return data


class Picture_table(QWidget):
    def __init__(self,number,datas):
        super().__init__()
        self.current_page = 0
        self.page_size = 10
        self.number=number
        self.datas=datas
        self.init_ui()

    def init_ui(self):
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['图片地址', '识别结果', '识别时间'])
        self.update_table()
        #self.datas=get_picture_usage_record(self.number)

        # Add page navigation buttons
        self.prev_button = QPushButton('Prev')
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel(f'Page {self.current_page+1}')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.page_label, alignment=Qt.AlignHCenter)
        button_layout.addWidget(self.next_button)

        # Add all widgets to the main layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_table(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(self.page_size)
        data_len=len(self.datas)
        if (self.current_page+1)* self.page_size >= data_len :
            if(data_len%10==0):
                min_len=10
            else :
                min_len=data_len
        else :
            min_len=10
        #data = [[random.randint(0, 100) for _ in range(5)] for _ in range(self.page_size)]
        for row in range((self.current_page)*self.page_size,(self.current_page)*self.page_size+min_len):
            self.table_widget.setItem(row, 0, QTableWidgetItem(self.datas[row]['picture_address']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(self.datas[row]['result']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(self.datas[row]['picturetime']))
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table()
            self.page_label.setText(f'Page {self.current_page+1}')

    def next_page(self):
        self.current_page += 1
        self.update_table()
        self.page_label.setText(f'Page {self.current_page+1}')

if __name__ == '__main__':
    app = QApplication([])
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    datas=get_picture_usage_record('18212139396')
    table = Picture_table('18212139396',datas)
    table.show()
    app.exec_()



