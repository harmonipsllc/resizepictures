from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QProgressBar, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
import sys
from controllers.main_controller import MainController
from utils.file_utils import FileUtils
import os

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        file_utils = FileUtils()
        self.controller = MainController(self, file_utils, self)
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Image Resizer App")
        # self.setGeometry(100, 100, 1200, 800)
        self.setAcceptDrops(True)

        self.status_label = QLabel("Drop a folder or files here", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        self.original_image_label = QLabel(self)
        self.resized_image_label = QLabel(self)

        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)
        self.prev_button.clicked.connect(self.controller.show_previous_image)
        self.next_button.clicked.connect(self.controller.show_next_image)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_image_label)
        image_layout.addWidget(self.resized_image_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        layout.addLayout(image_layout)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            directories = [path for path in paths if os.path.isdir(path)]
            files = [path for path in paths if os.path.isfile(path)]

            if directories:
                for directory in directories:
                    self.controller.load_images(directory, append=True)
            if files:
                self.controller.load_images(files, append=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())