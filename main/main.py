import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
from camera_worker import CameraWorker


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
        self.camera_worker.camera_data_ready.connect(self.camera_update_slot)
        self.camera_worker.start()

        self.run()

    def run(self):
        next

    def closeEvent(self, event=None):
        print("stopping program")
        self.camera_worker.stop()

    def camera_update_slot(self, frame):
        frame = self.camera_worker.scale_frame_to_label(self.ui.camera, frame)
        self.ui.camera.setPixmap(QPixmap.fromImage(frame))

    def clear_btn_clicked(self):
        next

    def reset_btn_clicked(self):
        # self.ui.output.setText("testing")
        self.ui.output.clear()

    def exit_btn_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec_())
