# -*- coding: utf-8 -*-
"""
Contains the class definition to predict hand landmarks using mediapipe
and predict hand sign based on hand landmarks using Pytorch neural network
model. The model currently predicts only LEFT hand sign and has 26 letters
prediction.
"""
import mediapipe as mp
import torch

# using GPU for neural network prediction
DEVICE = (
    torch.accelerator.current_accelerator().type
    if torch.accelerator.is_available()
    else "cpu"
)
print(f"Using {DEVICE} device")

MIN_DETECTION_CONFIDENCE = 0.6


class PredictionModel:
    def __init__(self):
        # Mediapipe lanndmarks detection
        self.__mp_hands__ = mp.solutions.hands
        self.__mp_drawing__ = mp.solutions.drawing_utils
        self.__mp_drawing_styles__ = mp.solutions.drawing_styles
        self.__hands__ = self.__mp_hands__.Hands(
            static_image_mode=True,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            max_num_hands=1,
        )

        # Pytorch neural net model detection
        self.__model__ = torch.jit.load("model.pth.rar")
        self.__model__.eval()
        self.__model__.to(DEVICE)

    def prediction(self, frame) -> (object, tuple, tuple, str):
        """
        Function to make hand landmarks prediction and
        hand sign prediction using a camera frame

        Args:
            frame (cv2 frame): frame collected from the camera.

        Returns:
            (object, tuple, tuple, str): return a cv2 frame with drawn
            landmarks,a tuple containing top left position of boundary box,
            a tuple containing bottom right position of boundary box,
            and predicted hand sign character from the model.

        """

        data_aux, x_, y_ = [], [], []
        top_left_boundary, bottom_right_boundary = (), ()
        H, W, channel = frame.shape
        results = self.__hands__.process(frame)
        # hand landmarks prediction for left hand only
        if (
            results.multi_hand_landmarks
            and results.multi_handedness[0].classification[0].label == "Left"
        ):
            for hand_landmarks in results.multi_hand_landmarks:
                # Drawing landmarks per displayed frame
                self.__mp_drawing__.draw_landmarks(
                    frame,  # image to draw
                    hand_landmarks,  # model output
                    self.__mp_hands__.HAND_CONNECTIONS,  # hand connections
                    self.__mp_drawing_styles__.get_default_hand_landmarks_style(),
                    self.__mp_drawing_styles__.get_default_hand_connections_style(),
                )

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            x_min, x_max = min(x_), max(x_)
            y_min, y_max = min(y_), max(y_)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - x_min)
                data_aux.append(y - y_min)

            # (x1, y1) is the top left corner of the box
            top_left_boundary = (int(x_min * W) - 10, int(y_min * H) - 10)
            # (x2, y2) is the bottom right corner of the box
            bottom_right_boundary = (int(x_max * W) - 10, int(y_max * H) - 10)

        return (
            frame,
            top_left_boundary,
            bottom_right_boundary,
            self.__hand_sign_prediction__(data_aux),
        )

    def __hand_sign_prediction__(self, data_aux: list) -> str:
        """
        Function to execute hand sign prediction using the neural network model

        Args:
            data_aux (list): list of hand landmarks detected using media pipe.

        Returns:
            str: the predicted character (A - Z).

        """

        if data_aux:
            with torch.no_grad():
                data_aux = torch.tensor(
                    data_aux, dtype=torch.float32
                ).flatten()
                predictions_log = self.__model__(
                    data_aux.unsqueeze(0).to(DEVICE)
                )
                predictions_prob = torch.exp(predictions_log)
                max_probability_predicted, max_probability_index = torch.max(
                    predictions_prob, dim=1
                )
                if max_probability_predicted.item() >= 0.15:
                    predicted_character = chr(
                        max_probability_index.item() + 65
                    )  # chr(65) = 'A'
                    return predicted_character
        return "None"

    def stop(self):
        del self.__model__
        torch.cuda.empty_cache()
