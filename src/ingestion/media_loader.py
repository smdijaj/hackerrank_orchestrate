from pathlib import Path
import pandas as pd


class MediaLoader:
    """
    Loads image and voice metadata from the dataset.
    """

    def __init__(self, dataset_path: Path):
        self.dataset_path = Path(dataset_path)

        self.images_df = None
        self.voice_df = None

    def load_images(self):
        """
        Load images.csv
        """
        image_file = self.dataset_path / "images.csv"

        try:
            self.images_df = pd.read_csv(image_file)
            print(f"[INFO] Loaded images.csv ({len(self.images_df)} records)")
            return self.images_df

        except Exception as e:
            print(f"[ERROR] Unable to load images.csv: {e}")
            return None

    def load_voice_notes(self):
        """
        Load voice_notes.csv
        """
        voice_file = self.dataset_path / "voice_notes.csv"

        try:
            self.voice_df = pd.read_csv(voice_file)
            print(f"[INFO] Loaded voice_notes.csv ({len(self.voice_df)} records)")
            return self.voice_df

        except Exception as e:
            print(f"[ERROR] Unable to load voice_notes.csv: {e}")
            return None

    def get_image_path(self, image_id):
        """
        Return image file path from image_id.
        """

        if self.images_df is None:
            self.load_images()

        row = self.images_df[self.images_df["image_id"] == image_id]

        if row.empty:
            return None

        return self.dataset_path / row.iloc[0]["file_path"]

    def get_voice_path(self, voice_id):
        """
        Return voice file path from voice_id.
        """

        if self.voice_df is None:
            self.load_voice_notes()

        row = self.voice_df[self.voice_df["voice_id"] == voice_id]

        if row.empty:
            return None

        return self.dataset_path / row.iloc[0]["file_path"]