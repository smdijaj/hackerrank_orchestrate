from pathlib import Path
import wave


class AudioPreprocessor:
    """
    Handles basic preprocessing of voice notes.
    """

    def __init__(self):
        pass

    def validate_audio(self, audio_path):
        """
        Check whether the audio file exists.
        """
        return Path(audio_path).exists()

    def get_audio_info(self, audio_path):
        """
        Return basic audio information.
        """

        try:
            with wave.open(str(audio_path), "rb") as audio:
                return {
                    "channels": audio.getnchannels(),
                    "sample_width": audio.getsampwidth(),
                    "frame_rate": audio.getframerate(),
                    "frames": audio.getnframes(),
                    "duration": round(
                        audio.getnframes() / audio.getframerate(),
                        2
                    )
                }

        except Exception as e:
            print(f"[ERROR] {e}")
            return None

    def preprocess(self, audio_path):
        """
        Complete preprocessing pipeline.
        """

        if not self.validate_audio(audio_path):
            print("[ERROR] Audio file not found.")
            return None

        return self.get_audio_info(audio_path)