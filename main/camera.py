# -*- coding: utf-8 -*-
"""
Contains the class definition to initiate the camera object using cv2.
Additionally, the class contains the hand landmarks mapping with mediapipe.
"""

import cv2
from PyQt5.QtGui import QImage
from prediction import PredictionModel
from typing import Optional


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.prediction_model = PredictionModel()

    def collect_frame(self) -> Optional[QImage]:
        """
        Function to get a frame from the main system camera, process landmarks,
        display landmarks, make prediction, display prediction, and
        return resulting image convereted to QImage frame for pyqt to display.

        Returns:
            qt_frame (QImage): a frame collected and processed by the mode
            converted to a QImage for pyqt.

        """

        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_flipped = cv2.flip(frame_rgb, 1)
            (
                frame_with_prediction,
                top_left_boundary,
                bottom_right_boundary,
                predicted_char,
            ) = self.prediction_model.prediction(frame_flipped)
            final_frame = self.draw_character_boundary(
                frame_with_prediction,
                top_left_boundary,
                bottom_right_boundary,
                predicted_char,
            )

            H, W, channel = final_frame.shape
            qt_frame = QImage(final_frame.data, W, H, QImage.Format_RGB888)
            return qt_frame

    def draw_character_boundary(
        self,
        frame,
        top_left_boundary: tuple,
        bottom_right_boundary: tuple,
        predicted_char: str,
    ) -> object:
        """
        Function to draw character boundary box for the given character based on
        top left point and bottom right point of the boundary box

        Args:
            frame (cv2 frame): frame processed from mediapipe model
            top_left_boundary (tuple): (x1, y1) position of the top left boundary box
            bottom_right_boundary (tuple): (x2, y2) position of the bottom right boundary box
            predicted_char (str): predicted character by the neural network model

        Returns:
            frame (cv2 frame): cv2 frame with drawn boundary box and predicted character

        """
        if top_left_boundary and bottom_right_boundary:
            x1, y1 = top_left_boundary
            x2, y2 = bottom_right_boundary

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(
                frame,
                predicted_char,
                (x2, y2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 0, 0),
                3,
                cv2.LINE_AA,
            )
        return frame

    def stop_camera(self) -> None:
        self.cap.release()
        self.prediction_model.stop()
        cv2.destroyAllWindows()
