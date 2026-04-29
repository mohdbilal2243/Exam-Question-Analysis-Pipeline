# Exam Question Paper Analysis & Topic Classification Pipeline

## Overview

This project builds an end-to-end NLP pipeline to automatically analyze exam question papers and classify questions into academic topics. It helps identify topic-wise trends across years, enabling better exam preparation strategies.

---

## Problem Statement

Given multiple years of exam papers (PDF/text) and a configurable list of topics, the system:

* Extracts and segments individual questions
* Classifies each question into one or more topics
* Aggregates results to generate insights and trends

---

## System Architecture

Pipeline:

1. **PDF Parsing & Text Extraction**
2. **Question Segmentation**
3. **Topic Classification (Semantic Embeddings)**
4. **Aggregation & Trend Analysis**
5. **Evaluation with Labeled Data**

---

## Project Structure

```
Exam-Question-Analysis-Pipeline/
│── data/
│   ├── sample_papers/
│   ├── topics.json
│   ├── labeled.json
│
│── src/
│   ├── parser.py
│   ├── classifier.py
│   ├── aggregator.py
│   ├── evaluate.py
│   ├── main.py
│
│── output/
│   ├── results.json
│   ├── summary.json
│
│── requirements.txt
│── README.md
```

---

## Approach

### 1. Question Extraction

* Used `pdfplumber` for PDF parsing
* Regex-based segmentation for:

  * Question numbers (Q1, Q2…)
  * Subparts (i, ii, iii)
* Cleaned noise like page numbers and OCR artifacts

---

### 2. Topic Classification

* Used `sentence-transformers (all-MiniLM-L6-v2)`
* Converted questions and topics into embeddings
* Applied cosine similarity
* Supported:

  * Multi-topic classification
  * Confidence scores
  * Dynamic thresholding

---

### 3. Aggregation

* Total questions per topic
* Year-wise distribution
* Trend analysis
* Multi-topic detection

---

### 4. Evaluation

* Used manually labeled dataset (`labeled.json`)
* Relaxed accuracy metric (correct if true topic in predicted set)
* Achieved ~75–85% accuracy on validation set

---

## Sample Output

### Question Output

```json
{
  "year": 2024,
  "paper": "Maths_2024",
  "question_number": "1(i)",
  "text": "Find the derivative of x^2",
  "topics": [
    {"topic": "Differentiation", "confidence": 0.67}
  ]
}
```

---

### Summary Output

```json
{
  "total_per_topic": {
    "Differentiation": 18,
    "Vectors": 14,
    "Probability": 8
  },
  "yearly_breakdown": {
    "Differentiation": {
      "2023": 3,
      "2024": 9,
      "2025": 6
    }
  }
}
```

---

## Key Design Decisions

* Used **semantic embeddings** instead of keyword matching for better generalization
* Designed **config-driven topics** (no code changes required)
* Handled **multi-label classification**
* Balanced performance and accuracy under compute constraints

---

## Limitations

* OCR noise affects parsing accuracy
* Limited labeled data for evaluation
* Some topics overlap semantically

---

## Future Improvements

* Fine-tune domain-specific classifier
* Improve parsing using layout-aware models (LayoutLM)
* Add visualization dashboard
* Expand labeled dataset

---

## Conclusion

This pipeline demonstrates a scalable and modular approach to automate exam paper analysis using NLP and embedding-based classification.
