from pathlib import Path


class AudioReasoner:
    """
    Analyzes voice note messages and extracts useful signals.
    """

    def __init__(self):
        pass


    def analyze(self, audio_path, audio_info=None):
        """
        Analyze voice note.
        """

        result = {
            "has_audio": True,
            "audio_exists": False,
            "duration": None,
            "signals": []
        }


        if audio_path is None:
            result["has_audio"] = False
            return result


        path = Path(audio_path)


        if not path.exists():
            return result


        result["audio_exists"] = True


        # Use information from audio_preprocessor
        if audio_info:

            result["duration"] = audio_info.get(
                "duration"
            )


            if result["duration"]:

                # Long voice notes may contain detailed information
                if result["duration"] > 120:
                    result["signals"].append(
                        "long_voice_note"
                    )

                # Very short voice notes are usually casual
                elif result["duration"] < 5:
                    result["signals"].append(
                        "short_voice_note"
                    )


        return result