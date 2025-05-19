"""
Contain class definition to initiate the prediction worker class to make
predicition for the hand landmarks and hand sign.
"""

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from prediction import PredictionModel


class PredictionWorker(QThread):
    hand_sign_prediction_ready = pyqtSignal(str)
    processed_frame_ready = pyqtSignal(object, tuple, tuple, str)

    def __init__(self):
        super().__init__()

        self.__prediction_model__ = PredictionModel()

    def predict_hand_sign(self, frame) -> None:
        (
            frame,
            top_left_boundary,
            bottom_right_boundary,
            predicted_hand_sign,
        ) = self.__prediction_model__.prediction(frame)

        self.processed_frame_ready.emit(
            frame,
            top_left_boundary,
            bottom_right_boundary,
            predicted_hand_sign,
        )
        self.hand_sign_prediction_ready.emit(predicted_hand_sign)

    def stop(self):
        self.__prediction_model__.stop()
