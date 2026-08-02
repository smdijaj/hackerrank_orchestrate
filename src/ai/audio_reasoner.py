from pathlib import Path


class AudioReasoner:
    """
    Analyzes voice note messages and extracts useful signals.
    """

    def __init__(self):
        pass


    def analyze(
        self,
        audio_path,
        audio_info=None
    ):

        result = {

            "has_audio": True,

            "audio_exists": False,

            "duration": None,

            "transcript": "",

            "signals": []

        }


        if audio_path is None:

            result["has_audio"] = False

            return result



        path = Path(audio_path)


        if not path.exists():

            return result



        result["audio_exists"] = True



        if audio_info:

            result["duration"] = audio_info.get(
                "duration"
            )


            transcript = audio_info.get(
                "transcript",
                ""
            )


            if transcript:

                transcript = transcript.lower()

                result["transcript"] = transcript



                categories = {


                    "payment": [
                        "payment",
                        "bill",
                        "invoice",
                        "money",
                        "amount",
                        "refund"
                    ],


                    "urgent": [
                        "urgent",
                        "emergency",
                        "asap",
                        "immediately"
                    ],


                    "event": [
                        "meeting",
                        "function",
                        "event",
                        "schedule"
                    ],


                    "promotion": [
                        "offer",
                        "sale",
                        "discount"
                    ]

                }



                for category, words in categories.items():

                    for word in words:

                        if word in transcript:

                            result["signals"].append(
                                category
                            )



            if result["duration"]:

                if result["duration"] > 120:

                    result["signals"].append(
                        "long_voice_note"
                    )


                elif result["duration"] < 5:

                    result["signals"].append(
                        "short_voice_note"
                    )



        return result