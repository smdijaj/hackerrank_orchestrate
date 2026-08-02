from pathlib import Path
from src.preprocessing.audio_preprocessor import AudioPreprocessor

processor = AudioPreprocessor()

audio_path = Path(r"C:\Users\mijaj\python\projects\hackerrank_orchestrate\dataset\media\audio\vn_001.mp3")

info = processor.preprocess(audio_path)

print(info)