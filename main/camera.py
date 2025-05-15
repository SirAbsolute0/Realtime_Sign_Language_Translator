# -*- coding: utf-8 -*-
"""
Contains the class definition to initiate the camera object using cv2.
Additionally, the class contains the hand landmarks mapping with mediapipe.
"""

import cv2
from PyQt5.QtGui import QImage
from prediciton import ModelPrediction


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.model_prediction = ModelPrediction()

    def collect_frame(self):
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

            qt_frame = QImage(frame_flipped.data, W, H, QImage.Format_RGB888)
            return qt_frame

    def stop_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
