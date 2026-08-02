import pandas as pd


output = pd.read_csv(
    "dataset/output.csv"
)

messages = pd.read_csv(
    "dataset/messages.csv"
)


print("Output rows:", len(output))

print("Messages rows:", len(messages))


print("\nMissing values:")
print(output.isnull().sum())


print("\nAction distribution:")
print(
    output["action"].value_counts()
)


print("\nMessage type distribution:")
print(
    output["message_type"].value_counts()
)


print("\nSample predictions:")
print(
    output.head(10)
)