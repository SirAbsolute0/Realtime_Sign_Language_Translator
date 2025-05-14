"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""
Contain class definition to initiate the camera worker for the main window. The class create a camera object and emit the data to as image to a label on
the main window.

""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import cv2


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
                frame = cv2.flip(frame, 1)
                H, W, channel = frame.shape
                qt_frame = QImage(frame_rgb.data, W, H, QImage.Format_RGB888)
                self.camera_data_ready.emit(qt_frame)

    def stop(self):
        print("stopping camera")
        self.thread_active = False
        self.cap.release()
        cv2.destroyAllWindows()

    def scale_frame_to_label(self, label, frame):
        return frame.scaled(
            label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
