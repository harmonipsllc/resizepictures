import os
import cv2
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class MainController:
    def __init__(self, main_window, file_utils, main_app):
        self.main_window = main_window
        self.file_utils = file_utils
        self.main_app = main_app
        self.current_index = 0
        self.image_files = []
        self.resized_images = []

    def load_images(self, paths, append=False):
        if isinstance(paths, list):
            new_image_files = paths
        else:
            new_image_files = self.file_utils.get_image_files(paths)

        if append:
            self.image_files.extend(new_image_files)
        else:
            self.image_files = new_image_files

        self.main_app.status_label.setText(f"Processing {len(self.image_files)} files")
        self.main_app.progress_bar.setMaximum(len(self.image_files))

        width, height = self.get_resolution()
        crop = self.ask_crop_or_resize()

        if not append:
            self.resized_images = []

        for i, image_file in enumerate(new_image_files):
            image = cv2.imread(image_file)
            if image is not None:
                resized_image = self.process_image(image, width, height, crop)
                self.resized_images.append(resized_image)
                self.save_image(resized_image, image_file)
            self.main_app.progress_bar.setValue(i + 1)

        self.current_index = 0
        self.show_image()

    def get_resolution(self):
        width, ok = QInputDialog.getInt(self.main_window, "Input Width", "Enter the width in pixels:", value=1920)
        if not ok:
            return None, None
        height, ok = QInputDialog.getInt(self.main_window, "Input Height", "Enter the height in pixels:", value=1080)
        if not ok:
            return None, None
        return width, height

    def ask_crop_or_resize(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Crop or Resize")
        msg_box.setText("Do you want to crop the images or just resize them?")
        crop_button = msg_box.addButton("Crop", QMessageBox.ActionRole)
        resize_button = msg_box.addButton("Resize", QMessageBox.ActionRole)
        msg_box.exec_()

        if msg_box.clickedButton() == crop_button:
            return True
        else:
            return False

    def process_image(self, image, width, height, crop):
        h, w = image.shape[:2]

        if crop:
            if h > w:
                # Resize the image to the desired width while maintaining aspect ratio
                new_width = width
                new_height = int(h * (width / w))
                resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Crop the height from the center
                center_y = new_height // 2
                half_height = height // 2
                cropped_image = resized_image[center_y - half_height:center_y + half_height, :]
            else:
                if w > width:
                    # Resize the image to the desired width while maintaining aspect ratio
                    new_width = width
                    new_height = int(h * (width / w))
                    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                else:
                    resized_image = image
                    new_height = h  # Ensure new_height is defined

                if new_height > height:
                    # Crop the height from the center
                    center_y = new_height // 2
                    half_height = height // 2
                    cropped_image = resized_image[center_y - half_height:center_y + half_height, :]
                else:
                    cropped_image = resized_image

            return cropped_image
        else:
            # Just resize the image to the desired resolution
            resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
            return resized_image

    def save_image(self, image, original_path):
        base, ext = os.path.splitext(original_path)
        save_path = f"{base}_resized.png"
        cv2.imwrite(save_path, image)

    def show_image(self):
        if self.image_files and self.resized_images:
            original_image_path = self.image_files[self.current_index]
            resized_image = self.resized_images[self.current_index]

            original_pixmap = QPixmap(original_image_path)
            resized_pixmap = self.convert_cv_to_pixmap(resized_image)

            self.main_app.original_image_label.setPixmap(original_pixmap.scaled(400, 400, Qt.KeepAspectRatio))
            self.main_app.resized_image_label.setPixmap(resized_pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def convert_cv_to_pixmap(self, cv_img):
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_img = QImage(cv_img.data.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(q_img)

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image()