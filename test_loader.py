from src.output.output_generator import OutputGenerator


generator = OutputGenerator(
    "dataset/output.csv"
)


generator.add_result(
    "msg_001",
    "notify",
    "urgent",
    "Important urgent message",
    0.95,
    "msg_10;msg_20"
)


generator.add_result(
    "msg_002",
    "mute",
    "spam",
    "Suspicious promotional message",
    0.90,
    "none"
)


generator.save()