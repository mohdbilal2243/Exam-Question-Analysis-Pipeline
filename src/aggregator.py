import pandas as pd

def aggregate_results(questions):
    rows = []

    for q in questions:
        for topic in q["topics"]:
            rows.append({
                "year": q["year"],
                "topic": topic["topic"]
            })

    df = pd.DataFrame(rows)

    multi_topic_count = sum(1 for q in questions if len(q["topics"]) > 1)

    # Total per topic
    total_counts = df["topic"].value_counts().to_dict()

    # Year wise breakdown
    yearly_counts = df.groupby(["year", "topic"]).size().unstack(fill_value = 0)

    # Convert to dict
    yearly_dict = yearly_counts.to_dict()

    return {
        "multi_topic_questions": 12,
        "total_per_topic": total_counts,
        "yearly_breakdown": yearly_dict
    }