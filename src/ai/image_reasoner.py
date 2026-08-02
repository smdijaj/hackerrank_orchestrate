from pathlib import Path
from PIL import Image
import pytesseract


class ImageReasoner:

    def analyze(self, image_path):

        result = {
            "has_image": True,
            "image_exists": False,
            "image_type": "unknown",
            "signals": [],
            "extracted_text": ""
        }


        if image_path is None:
            result["has_image"] = False
            return result


        path = Path(image_path)


        if not path.exists():
            return result


        result["image_exists"] = True


        try:

            image = Image.open(path)

            result["image_type"] = "image"


            text = pytesseract.image_to_string(
                image
            )


            text = text.lower()

            result["extracted_text"] = text



            categories = {

                "payment": [
                    "bill",
                    "invoice",
                    "payment",
                    "receipt",
                    "transaction",
                    "amount",
                    "due"
                ],


                "promotion": [
                    "offer",
                    "sale",
                    "discount",
                    "coupon",
                    "deal"
                ],


                "event": [
                    "event",
                    "meeting",
                    "function",
                    "schedule",
                    "notice"
                ],


                "urgent": [
                    "urgent",
                    "emergency",
                    "immediately",
                    "asap"
                ]

            }


            for category, words in categories.items():

                for word in words:

                    if word in text:

                        result["signals"].append(
                            category
                        )


        except Exception as e:

            result["signals"].append(
                "image_processing_failed"
            )


        return result