from pathlib import Path


class ImageReasoner:
    """
    Analyzes image messages and extracts useful signals.
    """

    def __init__(self):
        pass


    def analyze(self, image_path):
        """
        Analyze image file.
        """

        result = {
            "has_image": True,
            "image_exists": False,
            "image_type": "unknown",
            "signals": []
        }


        if image_path is None:
            result["has_image"] = False
            return result


        path = Path(image_path)


        if not path.exists():
            return result


        result["image_exists"] = True


        extension = path.suffix.lower()


        if extension in [
            ".png",
            ".jpg",
            ".jpeg"
        ]:
            result["image_type"] = "image"


        # Basic signals
        filename = path.name.lower()


        keywords = [
            "poster",
            "offer",
            "sale",
            "event",
            "notice",
            "bill",
            "invoice"
        ]


        for word in keywords:
            if word in filename:
                result["signals"].append(word)


        return result