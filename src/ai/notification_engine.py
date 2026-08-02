import re


class NotificationEngine:
    """
    Decides message routing:
    notify / digest / mute
    """


    def __init__(self):
        pass


    def detect_risk(self, text):

        if not text:
            return False

        risky_keywords = [
            "urgent payment",
            "verify account",
            "click here",
            "free money",
            "lottery",
            "otp",
            "password",
            "bank"
        ]

        text = text.lower()

        for word in risky_keywords:
            if word in text:
                return True

        return False



    def detect_urgency(self, text):

        if not text:
            return False

        urgent_words = [
            "urgent",
            "emergency",
            "immediately",
            "today",
            "deadline",
            "asap",
            "important"
        ]

        text = text.lower()

        return any(
            word in text
            for word in urgent_words
        )



    def classify_type(self, message):

        text = str(
            message.get("message_text", "")
        ).lower()


        if self.detect_risk(text):
            return "scam"


        if self.detect_urgency(text):
            return "urgent"


        if message.get("conversation_type") == "business":

            if any(
                word in text
                for word in [
                    "offer",
                    "sale",
                    "discount",
                    "coupon"
                ]
            ):
                return "promotion"

            return "business_update"



        if message.get("media_type") == "image":
            return "event"


        if message.get("forwarded_count", 0) > 0:
            return "forward"


        if len(text.strip()) < 5:
            return "greeting"


        return "personal"



    def decide_action(
        self,
        message_type,
        context
    ):


        # Safety first
        if message_type == "scam":
            return "mute"


        user = context.get(
            "user",
            {}
        )


        # User ignores many notifications
        if (
            user and
            user.get(
                "notifications_dismissed_30d",
                0
            ) > 50
        ):
            return "digest"


        if message_type in [
            "urgent",
            "payment",
            "personal"
        ]:
            return "notify"


        if message_type in [
            "promotion",
            "business_update",
            "event"
        ]:
            return "digest"


        return "mute"



    def generate_reason(
        self,
        action,
        message_type
    ):

        reasons = {

            "notify":
            f"Important {message_type} message requiring attention",

            "digest":
            f"Useful {message_type} message that can wait",

            "mute":
            f"Low priority or unsafe {message_type} message"

        }

        return reasons[action]



    def route(
        self,
        message,
        context
    ):

        message_type = self.classify_type(
            message
        )


        action = self.decide_action(
            message_type,
            context
        )


        reason = self.generate_reason(
            action,
            message_type
        )


        return {

            "action": action,

            "message_type": message_type,

            "reason": reason

        }