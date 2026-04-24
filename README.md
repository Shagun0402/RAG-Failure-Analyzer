# 🧠 RAG Failure Analyzer

> A production-style Retrieval-Augmented Generation (RAG) system that **doesn't just answer questions — it explains why it might be wrong.**

---

## 🚨 Why This Project Exists

Most RAG demos stop at:

```json
{ "answer": "..." }
```

But real-world systems fail silently.

This project is built around a different question:

> ❓ *What happens when retrieval fails?*

Instead of hiding failure, this system:

* Measures retrieval quality
* Diagnoses failure modes
* Surfaces confidence and reasoning

---

## 🔍 What It Does

Given a user query, the system returns:

```json
{
  "answer": "...",
  "retrieval_quality": "low",
  "failure_reason": "stale knowledge",
  "confidence": 0.42,
  "retrieved_chunks": [...],
  "debug": {
    "similarity_score": 0.31,
    "entity_coverage": 0.22,
    "freshness_score": 0.10
  }
}
```

---

## 🏗️ Architecture

```
User Query
   ↓
Query Analyzer
   ↓
Retriever (ChromaDB)
   ↓
Retrieval Evaluator  ⭐
   ↓
LLM Generator (LangChain)
   ↓
Failure Analyzer  ⭐
   ↓
API Response
```

---

## ⚙️ Tech Stack

* **FastAPI** — Backend API layer
* **LangChain** — RAG orchestration
* **ChromaDB** — Vector database
* **OpenAI / Azure OpenAI** — LLM
* **SentenceTransformers** — Embeddings (optional)
* **React (optional)** — Frontend UI

---

## 📊 Core Innovation: Retrieval Evaluation

Most systems retrieve.
This one **evaluates retrieval quality before generation.**

### Signals Computed

| Signal              | Description                     |
| ------------------- | ------------------------------- |
| Semantic Similarity | How close chunks are to query   |
| Entity Coverage     | Do chunks contain key entities? |
| Freshness           | How recent is the data?         |
| Diversity           | Are results redundant?          |

---

## 🚫 Failure Modes Detected

| Failure Type       | Description                                |
| ------------------ | ------------------------------------------ |
| Embedding Mismatch | Query and docs are semantically misaligned |
| Missing Context    | Relevant docs not retrieved                |
| Stale Knowledge    | Outdated information                       |
| No Retrieval       | Empty or weak results                      |
| Noisy Context      | Conflicting or redundant chunks            |

---

## 🧪 Example

### Query

> "What was the pricing trend of product X in 2024?"

### Output

```json
{
  "answer": "Insufficient data available.",
  "retrieval_quality": "low",
  "failure_reason": "stale knowledge",
  "confidence": 0.33
}
```

---

## 📦 Project Structure

```
rag-failure-analyzer/
│
├── ingestion/        # Document loading, chunking, embedding
├── retrieval/        # Vector search logic
├── evaluation/       # Retrieval scoring (core)
├── generation/       # LLM prompting
├── api/              # FastAPI routes
├── frontend/         # Chat UI (optional)
├── docker/           # Docker configs
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone Repo

```
git clone https://github.com/your-username/rag-failure-analyzer.git
cd rag-failure-analyzer
```

### 2. Set Environment Variables

```
OPENAI_API_KEY=your_key
```

### 3. Run with Docker

```
docker-compose up --build
```

### 4. Access API

```
http://localhost:8000/docs
```

---

## 📡 API Endpoints

### POST /query

Request:

```json
{ "query": "Your question here" }
```

Response:

* Answer
* Retrieval quality
* Failure reason
* Debug metrics

---

## 📈 Observability

* Request-level logging
* Retrieval scores tracking
* Latency measurement
* Debug mode for internal signals

---

## 🧠 Key Learnings

* RAG failures are **systematic, not random**
* Retrieval quality directly impacts hallucination
* Observability is critical for LLM systems
* Evaluation layers are as important as generation

---

## 🔮 Future Improvements

* Hybrid search (BM25 + vector)
* Reranking models
* Automated evaluation benchmarks
* Feedback loop for continuous improvement

---

## 🤝 Contributing

PRs welcome. Focus areas:

* Better scoring functions
* New failure detection heuristics
* UI improvements

---

## ⭐ Final Thought

> Most systems try to sound confident.
>
> This one tries to be **honest.**

---
