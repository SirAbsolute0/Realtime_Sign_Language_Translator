import sys
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui import Ui_window


class CameraWorker(QThread):
    camera_data_ready = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.thread_active = True
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.thread_active:
            ret, frame = self.cap.read()

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = frame_rgb
                # frame = cv2.flip(frame, 1)
                H, W, channel = frame.shape
                qt_frame = QImage(frame_rgb.data, W, H, QImage.Format_RGB888)
                scaled_qt_frame = qt_frame.scaled(
                    1211, 911, Qt.KeepAspectRatio
                )

                self.camera_data_ready.emit(scaled_qt_frame)

    def stop(self):
        print("stopping camera")
        self.thread_active = False
        self.cap.release()
        cv2.destroyAllWindows()


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Required to setup UI with designer
        self.ui = Ui_window()
        self.ui.setupUi(self)
        ####################

        # Initiate camera worker for camera live feed
        self.camera_worker = CameraWorker()
        self.camera_worker.camera_data_ready.connect(self.camera_update_slot)
        self.camera_worker.start()

        self.run()

    def run(self):
        next

    def closeEvent(self, event):
        print("stopping program")
        self.camera_worker.stop()

    def camera_update_slot(self, image):
        self.ui.camera_view.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
