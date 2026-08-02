class ConfidenceEngine:
    """
    Calculates confidence score for routing decisions.
    Value range: 0 to 1
    """

    def __init__(self):
        pass


    def calculate(
        self,
        action,
        message_type,
        context,
        evidence_ids=None
    ):

        score = 0.5


        # Strong safety decision
        if message_type == "scam":
            score += 0.35


        # Urgent messages are easier to classify
        elif message_type == "urgent":
            score += 0.25


        # Evidence improves confidence
        if evidence_ids:
            score += 0.15


        # User history availability
        if context.get("user"):
            score += 0.05


        # Avoid overconfidence
        if action == "digest":
            score -= 0.05


        if action == "mute":
            score += 0.05


        # Keep between 0 and 1
        score = max(
            0,
            min(score, 1)
        )


        return round(score, 2)