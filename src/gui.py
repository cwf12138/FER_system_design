import sys
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from PyQt5 import QtWidgets

sys.path.append(os.path.dirname(__file__) + '/ui')
from ui import UI

#*已编写更好的展示UI，所以当前UI已弃用，但保留
def load_cnn_model():
    """
    载入CNN模型
    :return:
    """
    from model import CNN3
    model = CNN3()
    model.load_weights('./models/cnn3_best_weights.h5')
    return model


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QMainWindow()
    model = load_cnn_model()
    ui = UI(form, model)   #穿主窗口以及训练的模型，这个地方就是可以操作的，可以让其他的按键来调用这个窗口界面（大概）
    form.show()
    sys.exit(app.exec_())
