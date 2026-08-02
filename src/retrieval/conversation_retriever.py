import pandas as pd
from pathlib import Path


class ConversationRetriever:

    def __init__(self, dataset_path):

        self.dataset_path = Path(dataset_path)

        self.message_history = pd.read_csv(
            self.dataset_path / "message_history.csv"
        )

        self.message_events = pd.read_csv(
            self.dataset_path / "message_events.csv"
        )

    def get_user_history(self, user_id):
        """
        Retrieve all historical messages for a user.
        """

        history = self.message_history[
            self.message_history["user_id"] == user_id
        ].copy()

        return history.sort_values(
            by="created_at",
            ascending=False
        )

    def get_same_sender_history(self, user_id, sender_user_id):

        history = self.message_history[
            (self.message_history["user_id"] == user_id) &
            (self.message_history["sender_user_id"] == sender_user_id)
        ].copy()

        return history.sort_values(
            by="created_at",
            ascending=False
        )

    def get_same_group_history(self, user_id, group_id):

        if pd.isna(group_id):
            return pd.DataFrame()

        history = self.message_history[
            (self.message_history["user_id"] == user_id) &
            (self.message_history["group_id"] == group_id)
        ].copy()

        return history.sort_values(
            by="created_at",
            ascending=False
        )

    def get_same_business_history(self, user_id, business_id):

        if pd.isna(business_id):
            return pd.DataFrame()

        history = self.message_history[
            (self.message_history["user_id"] == user_id) &
            (self.message_history["business_id"] == business_id)
        ].copy()

        return history.sort_values(
            by="created_at",
            ascending=False
        )

    def get_message_events(self, message_ids):
        """
        Retrieve user interaction events for historical messages.
        """

        if len(message_ids) == 0:
            return pd.DataFrame()

        return self.message_events[
            self.message_events["message_id"].isin(message_ids)
        ]

    def retrieve(self, current_message):
        """
        Main retrieval function.
        """

        user_id = current_message["user_id"]

        sender_id = current_message["sender_user_id"]

        group_id = current_message["group_id"]

        business_id = current_message["business_id"]

        user_history = self.get_user_history(user_id)

        sender_history = self.get_same_sender_history(
            user_id,
            sender_id
        )

        group_history = self.get_same_group_history(
            user_id,
            group_id
        )

        business_history = self.get_same_business_history(
            user_id,
            business_id
        )

        events = self.get_message_events(
            user_history["message_id"].tolist()
        )

        return {

            "user_history": user_history,

            "sender_history": sender_history,

            "group_history": group_history,

            "business_history": business_history,

            "events": events

        }