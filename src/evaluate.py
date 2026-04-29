import json
from classifier import TopicClassifier

classifier = TopicClassifier("data/topics.json")

with open("data/labeled.json") as f:
    data = json.load(f)

correct = 0

for item in data:
    preds = classifier.classify(item["text"])
    pred_topics = [p["topic"] for p in preds]

    print("\nQuestion:", item["text"])
    print("Actual:", item["topic"])
    print("Predicted:", pred_topics)

    if item["topic"] in pred_topics:
        correct += 1

accuracy = correct / len(data)

print(f"Accuracy: {accuracy:.2f}")