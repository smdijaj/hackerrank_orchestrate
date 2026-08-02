import pandas as pd
from pathlib import Path


class OutputGenerator:
    """
    Generates final output.csv in required format.
    """

    def __init__(self, output_path):

        self.output_path = Path(output_path)

        self.results = []


    def add_result(
        self,
        message_id,
        action,
        message_type,
        reason,
        confidence,
        evidence_message_ids
    ):

        self.results.append({

            "message_id": message_id,

            "action": action,

            "message_type": message_type,

            "reason": reason,

            "confidence": confidence,

            "evidence_message_ids":
                evidence_message_ids

        })


    def save(self):

        df = pd.DataFrame(
            self.results,
            columns=[
                "message_id",
                "action",
                "message_type",
                "reason",
                "confidence",
                "evidence_message_ids"
            ]
        )


        df.to_csv(
            self.output_path,
            index=False
        )


        print(
            f"[INFO] Output saved: {self.output_path}"
        )


    def get_dataframe(self):

        return pd.DataFrame(
            self.results
        )