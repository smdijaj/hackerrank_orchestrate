class ConfidenceEngine:
    """
    Generates calibrated confidence scores.
    """

    def calculate(
        self,
        action,
        message_type,
        context,
        evidence_ids=None
    ):

        scores = {

            "urgent": 0.90,

            "payment": 0.85,

            "scam": 0.95,

            "personal": 0.75,

            "business_update": 0.70,

            "promotion": 0.65,

            "forward": 0.60,

            "greeting": 0.55,

            "spam": 0.90,

            "event": 0.70,

            "unknown": 0.50

        }


        confidence = scores.get(
            message_type,
            0.50
        )


        # Evidence improves confidence

        if evidence_ids:
            confidence += 0.05


        # User context improves personalization

        if context.get("user"):
            confidence += 0.03


        # Keep range 0-1

        confidence = min(
            confidence,
            1.0
        )


        return round(
            confidence,
            2
        )