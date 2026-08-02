import pandas as pd
from pathlib import Path


class DataLoader:
    def __init__(self):
        pass

    def load_csv(self, file_path: Path):
        """
        Load a CSV file and return a pandas DataFrame.
        """
        try:
            df = pd.read_csv(file_path)
            print(f"[INFO] Loaded: {file_path.name}")
            print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            return df

        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")

        except Exception as e:
            print(f"[ERROR] {e}")

        return None