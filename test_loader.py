import pandas as pd

from src.retrieval.conversation_retriever import ConversationRetriever
from src.retrieval.ranking import EvidenceRanker


messages = pd.read_csv(
    "dataset/messages.csv"
)


retriever = ConversationRetriever(
    "dataset"
)


ranker = EvidenceRanker(
    top_k=3
)


row = messages.iloc[0]


result = retriever.retrieve(row)


evidence = ranker.rank(
    result["user_history"],
    result["events"]
)


print("Evidence IDs:")
print(evidence)