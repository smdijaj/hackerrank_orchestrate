import pandas as pd
from datetime import datetime
import re


class EvidenceRanker:

    def __init__(self, top_k=5):
        self.top_k = top_k



    def recency_score(self, created_at):

        try:

            message_time = pd.to_datetime(
                created_at
            )

            days_old = (
                datetime.now() -
                message_time.to_pydatetime()
            ).days


            return 1 / (1 + max(days_old, 0))


        except Exception:

            return 0



    def engagement_score(
        self,
        message_id,
        events
    ):


        if events.empty:
            return 0


        event = events[
            events["message_id"] == message_id
        ]


        if event.empty:
            return 0


        row = event.iloc[0]


        score = 0


        if row["message_opened"]:
            score += 0.3


        if row["message_replied"]:
            score += 0.6


        if row["notification_dismissed"]:
            score -= 0.3


        if row["muted_after_message"]:
            score -= 0.5


        if row["message_reported"]:
            score -= 1


        return score



    def similarity_score(
        self,
        current_text,
        history_text
    ):


        if not current_text or not history_text:
            return 0


        current_words = set(
            re.findall(
                r"\w+",
                str(current_text).lower()
            )
        )


        history_words = set(
            re.findall(
                r"\w+",
                str(history_text).lower()
            )
        )


        if not current_words:
            return 0


        intersection = (
            current_words &
            history_words
        )


        union = (
            current_words |
            history_words
        )


        return len(intersection) / max(
            len(union),
            1
        )



    def context_score(
        self,
        row,
        current_message
    ):

        score = 0


        # Same sender

        if (
            row.get("sender_user_id")
            ==
            current_message.get(
                "sender_user_id"
            )
        ):
            score += 0.5



        # Same business

        if (
            row.get("business_id")
            ==
            current_message.get(
                "business_id"
            )
            and
            row.get("business_id")
        ):
            score += 0.4



        # Same group

        if (
            row.get("group_id")
            ==
            current_message.get(
                "group_id"
            )
            and
            row.get("group_id")
        ):
            score += 0.3



        return score



    def calculate_score(
        self,
        row,
        events,
        current_message
    ):


        score = 0


        score += (
            self.recency_score(
                row["created_at"]
            )
            * 0.20
        )


        score += (
            self.engagement_score(
                row["message_id"],
                events
            )
            * 0.25
        )


        score += (
            self.context_score(
                row,
                current_message
            )
            * 0.35
        )


        score += (
            self.similarity_score(
                current_message.get(
                    "message_text",
                    ""
                ),
                row.get(
                    "message_text",
                    ""
                )
            )
            * 0.20
        )


        return score



    def rank(
        self,
        history_df,
        events,
        current_message=None
    ):


        if history_df.empty:

            return []


        history_df = history_df.copy()


        if current_message is None:

            current_message = {}



        history_df["score"] = history_df.apply(

            lambda row:

            self.calculate_score(
                row,
                events,
                current_message
            ),

            axis=1

        )


        ranked = history_df.sort_values(
            by="score",
            ascending=False
        )


        return (
            ranked
            .head(self.top_k)
            ["message_id"]
            .tolist()
        )