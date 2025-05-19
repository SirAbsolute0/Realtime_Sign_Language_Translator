import sys
from PyQt5.QtGui import QPixmap
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

        # Buttons slot assignment
        self.ui.clear_btn.clicked.connect(self.clear_btn_clicked)
        self.ui.reset_btn.clicked.connect(self.reset_btn_clicked)
        self.ui.exit_btn.clicked.connect(self.exit_btn_clicked)

        # Initiate camera worker for camera live feed
        self.camera_worker = CameraWorker()
        self.camera_worker.final_frame_ready.connect(self.camera_update_slot)
        self.camera_worker.start()

        # Initiate prediction worker for hand landmarks and hand sign prediction
        self.prediction_workder = PredictionWorker()
        # connect unprocessed cv2 frame to prediction worker for processing
        self.camera_worker.unprocessed_frame_ready.connect(
            self.prediction_workder.predict_hand_sign
        )
        self.prediction_workder.processed_frame_ready.connect(
            self.camera_worker.generate_final_frame
        )
        self.prediction_workder.hand_sign_prediction_ready.connect(
            self.prediction_slot
        )
        self.prediction_workder.start()

        # Initiate word search worker for live word auto complete base on input
        self.word_search_worker = WordSearchWorker()
        self.word_search_worker.auto_complete_result_ready.connect(
            self.word_search_slot
        )
        self.prediction_workder.hand_sign_prediction_ready.connect(
            self.word_search_worker.add_predicted_char
        )
        self.ui.word_choice.itemClicked.connect(
            self.word_choice_list_item_clicked
        )
        self.word_search_worker.start()

        self.run()

    def run(self):
        next

    def closeEvent(self, event=None) -> None:
        self.camera_worker.stop()
        self.prediction_workder.stop()
        self.word_search_worker.stop()

        self.camera_worker.wait()
        # word_search doesn't have a inf loop so no need to wait

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

    def prediction_slot(self) -> None:
        next

    def word_search_slot(self, word_list: list) -> None:
        """
        Slot function to handle updating the pyqt qlistwidget with the
        current auto completion list of words.

        Args:
            word_list (list): auto completed list of words for display.

        """

        self.ui.word_choice.addItems(word_list)

    def word_choice_list_item_clicked(self, word_item: object) -> None:
        """
        Linked the click of each word (item) on the qlistwidget to displaying
        the given word on the full result output qlabel.

        Args:
            word_item (object): qt object from the qlistwidget each is
            a word.
        """

        # self.text_output += word_item.text() + " "
        # self.ui.output.setText(self.text_output)
        next

    def clear_btn_clicked(self) -> None:
        next

    def reset_btn_clicked(self) -> None:
        self.text_output = ""
        self.ui.output.clear()

    def exit_btn_clicked(self) -> None:
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
