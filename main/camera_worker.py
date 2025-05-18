"""
Contain class definition to initiate the camera worker for the main window.
The class create a camera object and emit the data to as image to a label on
the main window.
"""

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from camera import Camera


class CameraWorker(QThread):
    camera_data_ready = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.__thread_active__ = True
        self.__camera__ = Camera()

    def run(self) -> None:
        while self.__thread_active__:
            frame = self.__camera__.collect_frame()
            if frame is not None:
                self.camera_data_ready.emit(frame)
        return

    def stop(self) -> None:
        self.__thread_active__ = False
        self.__camera__.stop_camera()

    @staticmethod
    def scale_frame_to_label(label: object, frame: QImage) -> QImage:
        """
        Function to be called from main to scale the video to the size
        of the displayed label at anytime.

        Args:
            label (QLabel): the label connected to the camera view.
            frame (Qimage frame): the current frame from the camera to be
            displayed on the label.

        Returns:
            Qimage frame: scaled camera frame to the label sizing.

        """
        # return frame
        return frame.scaled(
            label.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
