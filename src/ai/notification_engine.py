class NotificationEngine:
    """
    Personalized WhatsApp notification routing engine.
    """


    def __init__(self):
        pass


    def detect_scam(self, text, context):

        if not text:
            return False

        text = text.lower()

        scam_words = [
            "otp",
            "password",
            "verify account",
            "click here",
            "free money",
            "lottery",
            "bank details",
            "send money"
        ]

        if any(word in text for word in scam_words):
            return True


        business = context.get("business")


        if business:

            if (
                not business.get("verified", False)
                and
                business.get("user_reports_30d", 0) > 5
            ):
                return True


        return False



    def detect_spam(self, text):

        if not text:
            return False


        spam_words = [
            "subscribe",
            "win",
            "free",
            "offer",
            "discount",
            "sale",
            "coupon",
            "limited time"
        ]


        text = text.lower()


        return any(
            word in text
            for word in spam_words
        )



    def detect_payment(self, text):

        keywords = [
            "payment",
            "invoice",
            "bill",
            "refund",
            "transaction",
            "receipt",
            "due amount"
        ]


        text = text.lower()


        return any(
            word in text
            for word in keywords
        )



    def detect_urgent(self, text):

        keywords = [
            "urgent",
            "emergency",
            "asap",
            "deadline",
            "immediately",
            "important"
        ]


        text = text.lower()


        return any(
            word in text
            for word in keywords
        )



    def classify_type(
        self,
        message,
        context
    ):

        text = str(
            message.get(
                "message_text",
                ""
            )
        )


        if self.detect_scam(
            text,
            context
        ):
            return "scam"



        if self.detect_payment(text):
            return "payment"



        if self.detect_urgent(text):
            return "urgent"



        if message.get(
            "media_type"
        ) == "image":

            return "event"



        if message.get(
            "conversation_type"
        ) == "business":


            if self.detect_spam(text):

                return "promotion"


            return "business_update"



        if self.detect_spam(text):

            return "spam"



        if message.get(
            "forwarded_count",
            0
        ) > 0:

            return "forward"



        if len(text.strip()) < 5:

            return "greeting"



        if message.get(
            "conversation_type"
        ) == "personal":

            return "personal"



        return "unknown"



    def decide_action(
        self,
        message_type,
        context
    ):


        if message_type == "scam":

            return "mute"


        if message_type == "spam":

            return "mute"



        membership = context.get(
            "membership"
        )


        if membership:

            if membership.get(
                "group_muted_by_user",
                False
            ):

                if message_type not in [
                    "urgent",
                    "payment"
                ]:

                    return "digest"



        user = context.get(
            "user",
            {}
        )


        dismissed = user.get(
            "notifications_dismissed_30d",
            0
        )


        if dismissed > 50:

            return "digest"



        if message_type in [
            "urgent",
            "payment",
            "personal"
        ]:

            return "notify"



        if message_type in [
            "event",
            "business_update",
            "promotion",
            "forward",
            "greeting"
        ]:

            return "digest"



        return "mute"



    def generate_reason(
        self,
        message_type,
        action
    ):

        reasons = {

            "urgent":
            "Urgent message detected requiring immediate attention",

            "payment":
            "Payment-related message that may require user action",

            "scam":
            "Suspicious message detected due to safety risk",

            "personal":
            "Personal conversation likely relevant to the user",

            "business_update":
            "Business update from a known account suitable for later review",

            "promotion":
            "Promotional content with lower priority",

            "forward":
            "Forwarded content with reduced urgency",

            "spam":
            "Low-value or unwanted message detected",

            "greeting":
            "Casual greeting message",

            "event":
            "Event-related media message"

        }


        return reasons.get(
            message_type,
            f"{message_type} message routed as {action}"
        )



    def route(
        self,
        message,
        context
    ):


        message_type = self.classify_type(
            message,
            context
        )


        action = self.decide_action(
            message_type,
            context
        )


        reason = self.generate_reason(
            message_type,
            action
        )


        return {

            "action": action,

            "message_type": message_type,

            "reason": reason

        }