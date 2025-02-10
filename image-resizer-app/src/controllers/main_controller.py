import os
import cv2
from PyQt5.QtWidgets import QInputDialog, QFileDialog

class MainController:
    def __init__(self, main_window, file_utils, main_app):
        self.main_window = main_window
        self.file_utils = file_utils
        self.main_app = main_app

    def load_images(self, paths):
        if isinstance(paths, list):
            image_files = paths
        else:
            image_files = self.file_utils.get_image_files(paths)

        self.main_app.status_label.setText(f"Processing {len(image_files)} files")
        self.main_app.progress_bar.setMaximum(len(image_files))

        width, height = self.get_resolution()

        for i, image_file in enumerate(image_files):
            image = cv2.imread(image_file)
            if image is not None:
                resized_image = self.process_image(image, width, height)
                self.save_image(resized_image, image_file)
            self.main_app.progress_bar.setValue(i + 1)

    def get_resolution(self):
        width, ok = QInputDialog.getInt(self.main_window, "Input Width", "Enter the width in pixels:", value=1920)
        if not ok:
            return None, None
        height, ok = QInputDialog.getInt(self.main_window, "Input Height", "Enter the height in pixels:", value=1080)
        if not ok:
            return None, None
        return width, height

    def process_image(self, image, width, height):
        h, w = image.shape[:2]

        if w > width or h > height:
            # Crop the image from the center
            center_x, center_y = w // 2, h // 2
            half_width, half_height = width // 2, height // 2
            cropped_image = image[center_y - half_height:center_y + half_height, center_x - half_width:center_x + half_width]
        else:
            # Resize the image to the desired resolution
            cropped_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

        return cropped_image

    def save_image(self, image, original_path):
        base, ext = os.path.splitext(original_path)
        save_path = f"{base}_resized.png"
        cv2.imwrite(save_path, image)