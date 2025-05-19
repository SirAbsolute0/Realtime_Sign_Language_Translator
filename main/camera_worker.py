"""
Contain class definition to initiate the camera worker for the main window.
The class create a camera object and emit the data to as image to a label on
the main window.
"""

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from camera import Camera
import time


class CameraWorker(QThread):
    # cv2 frame to be sent to prediction_worker for processing
    unprocessed_frame_ready = pyqtSignal(object)
    # final frame to be sent to main for displaying
    final_frame_ready = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.__thread_active__ = True
        self.__camera__ = Camera()
        self.__final_frame__ = None

    def run(self) -> None:
        while self.__thread_active__:
            frame = self.__camera__.collect_frame()
            if frame is not None:
                self.unprocessed_frame_ready.emit(frame)
                time.sleep(0.1)
                if self.__final_frame__ is not None:
                    self.final_frame_ready.emit(self.__final_frame__)
                    self.__final_frame__ = None
        return

    def collect_processed_frame(
        self,
        frame: object,
        top_left_boundary: tuple,
        bottom_right_boundary: tuple,
        predicted_char: str,
    ) -> None:
        self.__final_frame__ = self.__camera__.collect_processed_frame(
            frame, top_left_boundary, bottom_right_boundary, predicted_char
        )

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
