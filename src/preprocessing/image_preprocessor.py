from pathlib import Path
from PIL import Image


class ImagePreprocessor:
    """
    Handles basic preprocessing of image files.
    """

    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size

    def load_image(self, image_path):
        """
        Load an image from disk.
        """
        try:
            image = Image.open(image_path).convert("RGB")
            return image
        except Exception as e:
            print(f"[ERROR] Unable to load image: {e}")
            return None

    def resize_image(self, image):
        """
        Resize image.
        """
        if image is None:
            return None

        return image.resize(self.image_size)

    def preprocess(self, image_path):
        """
        Complete preprocessing pipeline.
        """
        image = self.load_image(image_path)

        if image is None:
            return None

        image = self.resize_image(image)

        return image