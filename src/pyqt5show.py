import sys
import cv2
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from recognition_camera import predict_expression
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, frame):
        super().__init__()
        self._run_flag = True
        self.frame = frame

    def run(self):
        while self._run_flag:
            rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            self.change_pixmap_signal.emit(p)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self, frame):
        super().__init__()

        self.thread = VideoThread(frame)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        # Set up the GUI
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.button = QPushButton('Quit', self)
        self.button.clicked.connect(self.close)
        self.show()

    def update_image(self, pixmap):
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame=predict_expression()
    window = MainWindow(frame) # Pass your video stream frame here
    sys.exit(app.exec_())
