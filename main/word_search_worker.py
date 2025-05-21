# -*- coding: utf-8 -*-
"""
File contains class definition for word search worker to do work search
concurrently on another thread with other parts of the software
"""

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from word_search import WordSearch

HAND_SIGN_DETERMINATION_TIME_LIMIT = 120


class WordSearchWorker(QThread):
    auto_complete_result_ready = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.__last_predicted_char__ = "None"
        self.__counter__ = 0
        self.__current_word__ = ""
        self.__word_search__ = WordSearch()

    def __display_possible_words__(self) -> None:
        """
        Function to emit the list of auto completion words of the given word
        generated from hand sign.

        """

        result = self.__word_search__.auto_complete_word(self.__current_word__)
        self.auto_complete_result_ready.emit(result)

    @pyqtSlot(str)
    def add_predicted_char(self, predicted_char: str) -> None:
        """
        Function to keep track of last predicted character and current
        predicted character. If they remain the same and not None for a
        pre-determined time counter. It consider a valid character and is added
        to the current word.

        Args:
            predicted_char (str): predicted hand sign character given by
            prediction worker from the given camera frame.

        """

        if (
            predicted_char == self.__last_predicted_char__
            and predicted_char != "None"
        ):
            self.__counter__ += 1
            if self.__counter__ >= HAND_SIGN_DETERMINATION_TIME_LIMIT:
                self.__current_word__ += predicted_char.lower()
                self.__display_possible_words__()

                self.__counter__ = 0
        else:
            self.__counter__ = 0

        self.__last_predicted_char__ = predicted_char

    @pyqtSlot()
    def clear_current_word(self) -> None:
        """
        Function to clear out the current word.

        """

        self.__current_word__ = ""

    def stop(self):
        del self.__word_search__
