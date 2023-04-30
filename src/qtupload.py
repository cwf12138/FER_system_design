from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout
import sys
from recognition_camera import App
from model import CNN2, CNN3
def load_model():
    """
    加载本地模型
    :return:
    """
    model = CNN3()
    model.load_weights('./models/cnn3_best_weights.h5')
    return model
class MainWindow(QWidget):
    def __init__(self,model):
        super().__init__()

        self.video_path = ""
        self.model=model
        # 创建控件
        self.button_upload = QPushButton('上传视频')
        self.label_path = QLabel("")
        self.button_video=QPushButton('人脸检测')
        # 设置布局
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.button_upload)
        self.vbox.addWidget(self.button_video)
        self.vbox.addWidget(self.label_path)
        self.setLayout(self.vbox)

        # 绑定事件
        self.button_upload.clicked.connect(self.get_video_path)
        self.button_video.clicked.connect(self.use_recognition)


    def get_video_path(self):
        filename, _ = QFileDialog.getOpenFileName(self, "上传视频", "", "Video Files (*.mp4 *.avi)")
        if filename:
            self.video_path = filename
            self.label_path.setText(f"已选择：{filename}")
    def use_recognition(self):
        app=App(model,self.video_path)
        app.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model=load_model()
    window = MainWindow(model)
    window.show()
    sys.exit(app.exec_())
