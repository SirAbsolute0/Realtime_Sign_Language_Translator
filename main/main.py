from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, Qt, QThread, pyqtSlot
import cv2
from gui import Ui_window


class CameraWorker(QThread):
    def __init_(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.camera_data_ready = pyqtSignal()

    @pyqtSlot()
    def run(self):
        while True:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            H, W, channel = frame.shape

            # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # cv2.imshow('frame', frame)
            self.camera_data_ready.emit(frame)

    def stop(self):
        print("stopping camera")
        self.cap.release()
        cv2.destroyAllWindows()


class RealTimeSignRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Required to setup UI with designer
        self.ui = Ui_window()
        self.ui.setupUi(self)
        ####################

        self.camera_worker = CameraWorker()

        self.run()

    def run(self):
        self.camera_worker.connect(
            self.ui.cameraView.camera_data_ready.display_image,
            type=Qt.ConnectionType.UniqueConnection,
        )

    def closeEvent(self):
        print("stopping program")
        self.camera_worker.stop()
        exit()
