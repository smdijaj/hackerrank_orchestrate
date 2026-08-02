from src.ai.image_reasoner import ImageReasoner

reasoner = ImageReasoner()

result = reasoner.analyze(
    "dataset/media/images/img_001.jpg"
)

print(result)