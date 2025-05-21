# -*- coding: utf-8 -*-
"""
Contains the class definition to initiate the camera object using cv2.
Additionally, the class contains the hand landmarks mapping with mediapipe.
"""

import cv2
from PyQt5.QtGui import QImage
from typing import Optional


class Camera:
    def __init__(self):
        self.__cap__ = cv2.VideoCapture(0)

    def collect_frame(self) -> Optional[object]:
        """
        Function to get a frame from the main system camera and flip it.

        Returns:
            object (cv2 frame): a frame collected by camera

        """

        ret, frame = self.__cap__.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_flipped = cv2.flip(frame_rgb, 1)
            return frame_flipped

    def generate_final_frame(
        self,
        frame: object,
        top_left_boundary: tuple,
        bottom_right_boundary: tuple,
        predicted_char: str,
    ) -> QImage:
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
        Return:
            qt_frame (QImage): final QImage to be displayed

        """
        final_frame = self.__draw_character_boundary__(
            frame,
            top_left_boundary,
            bottom_right_boundary,
            predicted_char,
        )

        H, W, channel = final_frame.shape
        qt_frame = QImage(final_frame.data, W, H, QImage.Format_RGB888)
        return qt_frame

    def __draw_character_boundary__(
        self,
        frame,
        top_left_boundary: tuple,
        bottom_right_boundary: tuple,
        predicted_char: str,
    ) -> object:
        """
        Function to draw character boundary box for the given character
        based on top left point and bottom right point of the boundary box

        Args:
            frame (cv2 frame): frame processed from mediapipe model
            top_left_boundary (tuple): (x1, y1) position of the top left
            boundary box
            bottom_right_boundary (tuple): (x2, y2) position of the bottom
            right boundary box
            predicted_char (str): predicted character by the neural network
            model

        Returns:
            frame (cv2 frame): cv2 frame with drawn boundary box and
            predicted character

        """
        if top_left_boundary and bottom_right_boundary:
            x1, y1 = top_left_boundary
            x2, y2 = bottom_right_boundary

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
            cv2.putText(
                frame,
                predicted_char,
                (x2, y2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (255, 0, 0),
                3,
                cv2.LINE_AA,
            )
        return frame

    def stop(self) -> None:
        self.__cap__.release()
        cv2.destroyAllWindows()
