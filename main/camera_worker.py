"""
Contain class definition to initiate the camera worker for the main window.
The class create a camera object and emit the data to as image to a label on
the main window.
"""

from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from camera import Camera


class CameraWorker(QThread):
    # cv2 frame to be sent to prediction_worker for processing
    unprocessed_frame_ready = pyqtSignal(object)
    # final frame to be sent to main for displaying
    final_frame_ready = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.__thread_active__ = True
        self.__new_frame__ = True
        self.__camera__ = Camera()

    def run(self) -> None:
        while self.__thread_active__:
            frame = self.__camera__.collect_frame()
            if frame is not None and self.__new_frame__:
                # send cv2 frame to prediction_worker for processing
                self.unprocessed_frame_ready.emit(frame)
        return

    @pyqtSlot(object, tuple, tuple, str)
    def generate_final_frame(
        self,
        frame: object,
        top_left_boundary: tuple,
        bottom_right_boundary: tuple,
        predicted_char: str,
    ) -> None:
        """
        Function to generate final frame with the processed cv2 frame with
        prediction from prediction_worker.

        Args:
            frame (cv2 frame): processed cv2 frame with hand landmarks and
            hand sign prediction
            top_left_boundary (tuple): top left boundary box (x1, y1)
            pixel coordinates
            bottom_right_boundary (tuple): bottom right boundary box (x2, y2)
            pixel coordinates
            predicted_char (str): predicted hand sign character

        """
        self.__new_frame__ = False
        final_frame = self.__camera__.generate_final_frame(
            frame, top_left_boundary, bottom_right_boundary, predicted_char
        )
        self.final_frame_ready.emit(final_frame)
        self.__new_frame__ = True

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

    def stop(self) -> None:
        self.__thread_active__ = False
        self.__camera__.stop()
