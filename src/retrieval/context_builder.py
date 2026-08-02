import pandas as pd
from pathlib import Path


class ContextBuilder:

    def __init__(self, dataset_path):

        self.dataset_path = Path(dataset_path)

        self.users = pd.read_csv(self.dataset_path / "users.csv")

        self.groups = pd.read_csv(self.dataset_path / "groups.csv")

        self.group_members = pd.read_csv(
            self.dataset_path / "group_members.csv"
        )

        self.business_accounts = pd.read_csv(
            self.dataset_path / "business_accounts.csv"
        )

        self.user_business_history = pd.read_csv(
            self.dataset_path / "user_business_history.csv"
        )

        self.daily_summary = pd.read_csv(
            self.dataset_path / "daily_notification_summary.csv"
        )

    def get_user_context(self, user_id):

        user = self.users[
            self.users["user_id"] == user_id
        ]

        if user.empty:
            return None

        return user.iloc[0].to_dict()

    def get_group_context(self, group_id):

        if pd.isna(group_id):
            return None

        group = self.groups[
            self.groups["group_id"] == group_id
        ]

        if group.empty:
            return None

        return group.iloc[0].to_dict()

    def get_group_membership(self, user_id, group_id):

        if pd.isna(group_id):
            return None

        membership = self.group_members[
            (self.group_members["user_id"] == user_id)
            &
            (self.group_members["group_id"] == group_id)
        ]

        if membership.empty:
            return None

        return membership.iloc[0].to_dict()

    def get_business_context(self, business_id):

        if pd.isna(business_id):
            return None

        business = self.business_accounts[
            self.business_accounts["business_id"] == business_id
        ]

        if business.empty:
            return None

        return business.iloc[0].to_dict()

    def get_user_business_history(self, user_id, business_id):

        if pd.isna(business_id):
            return None

        history = self.user_business_history[
            (self.user_business_history["user_id"] == user_id)
            &
            (self.user_business_history["business_id"] == business_id)
        ]

        if history.empty:
            return None

        return history.iloc[0].to_dict()

    def get_notification_summary(self, user_id):

        summary = self.daily_summary[
            self.daily_summary["user_id"] == user_id
        ]

        if summary.empty:
            return []

        return summary.to_dict("records")

    def build_context(
        self,
        user_id,
        group_id=None,
        business_id=None
    ):

        return {

            "user": self.get_user_context(user_id),

            "group": self.get_group_context(group_id),

            "membership": self.get_group_membership(
                user_id,
                group_id
            ),

            "business": self.get_business_context(
                business_id
            ),

            "business_history":
            self.get_user_business_history(
                user_id,
                business_id
            ),

            "notification_summary":
            self.get_notification_summary(
                user_id
            )
        }