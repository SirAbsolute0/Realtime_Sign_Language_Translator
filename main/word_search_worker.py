# -*- coding: utf-8 -*-
"""
File contains class definition for word search worker to do work search
concurrently on another thread with other parts of the software
"""

from PyQt5.QtCore import QThread, pyqtSignal
from word_search import WordSearch


class WordSearchWorker(QThread):
    auto_complete_result_ready = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.char_dict = {}
        self.word_search = WordSearch()

    def display_possible_words(self, curr_word_input: str) -> None:
        result = self.word_search.auto_complete_word(curr_word_input)
        self.auto_complete_result_ready.emit(result)

    def stop(self):
        del self.word_search
