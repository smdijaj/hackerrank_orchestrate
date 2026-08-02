import pandas as pd
from datetime import datetime


class EvidenceRanker:

    def __init__(self, top_k=5):
        self.top_k = top_k


    def recency_score(self, created_at):
        """
        Recent messages get higher priority.
        """

        try:
            message_time = pd.to_datetime(created_at)

            days_old = (
                datetime.now() - message_time.to_pydatetime()
            ).days

            score = 1 / (1 + max(days_old, 0))

            return score

        except Exception:
            return 0


    def engagement_score(self, message_id, events):
        """
        User interaction based score.
        """

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
            score += 0.5

        if row["notification_dismissed"]:
            score -= 0.3

        if row["muted_after_message"]:
            score -= 0.5

        if row["message_reported"]:
            score -= 1


        return score



    def calculate_score(self, row, events):

        score = 0


        # Recent interaction
        score += (
            self.recency_score(
                row["created_at"]
            )
            * 0.4
        )


        # User behaviour
        score += (
            self.engagement_score(
                row["message_id"],
                events
            )
            * 0.6
        )


        return score



    def rank(self, history_df, events):

        if history_df.empty:
            return []


        history_df = history_df.copy()


        history_df["score"] = history_df.apply(
            lambda row:
            self.calculate_score(
                row,
                events
            ),
            axis=1
        )


        ranked = history_df.sort_values(
            by="score",
            ascending=False
        )


        evidence_ids = (
            ranked
            .head(self.top_k)["message_id"]
            .tolist()
        )


        return evidence_ids