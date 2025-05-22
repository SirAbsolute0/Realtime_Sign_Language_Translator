import sys
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
from camera_worker import CameraWorker
from word_search_worker import WordSearchWorker
from prediciton_worker import PredictionWorker


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Required to setup UI with designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ####################

        # Set Qlabel properties
        self.ui.output.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Buttons slot assignment
        self.ui.clear_btn.clicked.connect(self.clear_btn_clicked)
        self.ui.reset_btn.clicked.connect(self.reset_btn_clicked)
        self.ui.exit_btn.clicked.connect(self.exit_btn_clicked)

        # Initiate camera worker for camera live feed
        self.camera_worker = CameraWorker()
        self.camera_worker.final_frame_ready.connect(self.camera_update_slot)
        self.camera_worker.start()

        # Initiate prediction worker for hand landmarks and sign prediction
        self.prediction_workder = PredictionWorker()
        # connect unprocessed cv2 frame to prediction worker for processing
        self.camera_worker.unprocessed_frame_ready.connect(
            self.prediction_workder.predict_hand_sign
        )
        self.prediction_workder.processed_frame_ready.connect(
            self.camera_worker.generate_final_frame
        )
        self.prediction_workder.start()

        # Initiate word search worker for word auto complete based on input
        self.word_search_worker = WordSearchWorker()
        self.word_search_worker.auto_complete_result_ready.connect(
            self.word_search_slot
        )
        self.prediction_workder.hand_sign_prediction_ready.connect(
            self.word_search_worker.add_predicted_char
        )
        self.ui.word_choice.itemClicked.connect(self.word_list_item_clicked)
        self.word_search_worker.start()

    def closeEvent(self, event=None) -> None:
        workers = [
            self.camera_worker,
            self.prediction_workder,
            self.word_search_worker,
        ]
        self.shutdown_workers(workers)

    def shutdown_workers(self, workers: list[object]) -> None:
        """
        Function to gracefully end all threads and their class objects

        Args:
            workers (list[QThread]): Qthread workers currently running.

        """

        for worker in workers:
            worker.stop()
            worker.quit()

        for worker in workers:
            if worker.isRunning():
                worker.wait()

    def camera_update_slot(self, frame) -> None:
        """
        Slot function to handle updating the pyqt  qlabel with the live
        camera feed

        Args:
            frame (QImage): frame processed with prediction and boundary
            detection box.

        """

        frame = CameraWorker.scale_frame_to_label(self.ui.camera, frame)
        self.ui.camera.setPixmap(QPixmap.fromImage(frame))

    def word_search_slot(self, word_list: list) -> None:
        """
        Slot function to handle updating the pyqt qlistwidget with the
        current auto completion list of words.

        Args:
            word_list (list): auto completed list of words for display.

        """
        self.signal_chosen_character_flash_screen()
        self.ui.word_choice.clear()
        self.ui.word_choice.addItems(word_list)

    def word_list_item_clicked(self, word_item: object) -> None:
        """
        Linked the click of each word (item) on the qlistwidget to displaying
        the given word on the full result output qlabel.

        Args:
            word_item (object): qt object from the qlistwidget each is
            a word.
        """
        text_output = self.ui.output.text()
        word = word_item.text()

        if text_output == "":
            word = word.capitalize()

        text_output += word + " "
        self.ui.output.setText(text_output)
        self.clear_btn_clicked()

    def signal_chosen_character_flash_screen(self) -> None:
        """
        Function to quickly flash the camera live view signalling a character
        has been chosen for the word

        """

        pixmap = QPixmap(self.ui.camera.size())
        pixmap.fill(QColor("white"))
        self.ui.camera.setPixmap(pixmap)

    def clear_btn_clicked(self) -> None:
        """
        Function to clear out the word choice list and the current word being
        searched.

        """

        self.ui.word_choice.clear()
        self.word_search_worker.clear_current_word()

    def reset_btn_clicked(self) -> None:
        """
        Function to reset the final output, clear word choice, and clear
        current word being searched

        """

        self.ui.output.clear()
        self.clear_btn_clicked()

    def exit_btn_clicked(self) -> None:
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
