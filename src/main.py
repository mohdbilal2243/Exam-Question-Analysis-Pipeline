from parser import parse_pdf
from classifier import TopicClassifier
from aggregator import aggregate_results
import os
import json

DATA_PATH = "data/sample_papers"
OUTPUT_PATH = "output/results.json"

classifier = TopicClassifier("data/topics.json")

all_questions = []

for file in os.listdir(DATA_PATH):
    if file.endswith(".pdf"):
        path = os.path.join(DATA_PATH, file)

        questions = parse_pdf(path)

        for q in questions:
            q["topics"] = classifier.classify(q["text"])

        all_questions.extend(questions)

        summary = aggregate_results(all_questions)

# Save output
os.makedirs("output", exist_ok=True)

# Save detailed results
with open("output/results.json", "w") as f:
    json.dump(all_questions, f, indent=4)

# Save summary
with open("output/summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("Pipeline completed")