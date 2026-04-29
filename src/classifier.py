from sentence_transformers import SentenceTransformer, util
import json
import torch

class TopicClassifier:
    def __init__(self, config_path, threshold = 0.4, top_k = 2):
        # load Topics
        with open(config_path, "r") as f:
            self.topics = json.load(f)["topics"]

        self.threshold = threshold
        self.top_k = top_k

        # Load Model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Precompute topic embeddings
        self.topic_embeddings = self.model.encode(
            self.topics, convert_to_tensor = True, normalize_embeddings = True
        )

    def classify(self, text):
        if not text.strip():
            return [{"topic": "Unclassified", "confidence": 0.0}]

        # Encode Question
        q_embedding = self.model.encode(
            text, convert_to_tensor = True, normalize_embeddings = True
        )

        # Cosine similarity
        scores = util.cos_sim(q_embedding, self.topic_embeddings)[0]

        # Get top-k matches
        top_results = torch.topk(scores, k = min(self.top_k, len(self.topics)))

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            score_val = float(score)

            dynamic_threshold = max(self.threshold, float(top_results.values[0]) * 0.6)

            if score_val >= dynamic_threshold:
                results.append({
                    "topic": self.topics[int(idx)],
                    "confidence": round(score_val, 3)
                })

        # If one topic is very strong, keep only that
        if len(results) > 1 and results[0]["confidence"] > 0.7:
            results = [results[0]]

        # Handle no match
        if not results:
            # fallback assign best topic even if low confidence
            best_idx = int(top_results.indices[0])
            best_score = float(top_results.values[0])

            return [{
                "topic": self.topics[best_idx],
                "confidence": round(best_score, 3)
            }]
        return results
