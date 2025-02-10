class ImageService:
    def __init__(self):
        pass

    def resize_image(self, image, target_size):
        import cv2

        height, width = image.shape[:2]
        target_width, target_height = target_size

        aspect_ratio = width / height

        if width > target_width or height > target_height:
            if aspect_ratio > 1:  # Wider than tall
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:  # Taller than wide
                new_height = target_height
                new_width = int(target_height * aspect_ratio)

            resized_image = cv2.resize(image, (new_width, new_height))
            return self.crop_center(resized_image, target_size)
        else:
            return cv2.resize(image, target_size)

    def crop_center(self, image, target_size):
        height, width = image.shape[:2]
        target_width, target_height = target_size

        start_x = width // 2 - target_width // 2
        start_y = height // 2 - target_height // 2

        return image[start_y:start_y + target_height, start_x:start_x + target_width]

    def process_images(self, image_paths, target_size):
        import cv2
        processed_images = []

        for path in image_paths:
            image = cv2.imread(path)
            if image is not None:
                processed_image = self.resize_image(image, target_size)
                processed_images.append(processed_image)

        return processed_images