import os

class FileUtils:
    def __init__(self):
        pass

    def get_image_files(self, folder_path):
        supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]
        return image_files