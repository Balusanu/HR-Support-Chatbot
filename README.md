# 🏢 HR Support Chatbot – Enterprise RAG System with LLMOps

## 📌 Problem Statement

Build a Retrieval-Augmented Generation (RAG) chatbot that retrieves context from internal HR policy documents and responds accurately to employee queries.

The chatbot:
- Retrieves relevant policy content
- Generates grounded responses
- Provides source transparency
- Monitors performance using LLM observability tools

---

# 📂 Data Collection

Collected and customized **11 HR Policy Documents**:

1. Attendance Policy  
2. Benefits & Perks Policy  
3. Code of Conduct  
4. Leave Policy  
5. Overtime Policy  
6. Referral Policy  
7. Reimbursement Policy  
8. Remote Work Policy  
9. Sexual Harassment Policy  
10. Work From Home Policy  
11. Performance Appraisal Policy  

### Customization Performed
Policies were modified to simulate a real enterprise environment:

- Company name: **A1B2C3 Pvt Ltd**
- Effective date: **01-01-2026**
- Work timings
- Reimbursement limits
- Leave structure
- Compensation details

---

# 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| Backend API | FastAPI + Uvicorn |
| Data Validation | Pydantic |
| Frontend | Streamlit + Requests |
| LLM Framework | LangChain |
| LLM Observability | LangSmith |
| LLM Inference | Groq |
| Embeddings | HuggingFace (BAAI/bge-large-en) |
| Reranking Model | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| Vector Database | ChromaDB |
| LLM Model | llama-3.3-70b-versatile |

---

# 🚀 Version Evolution

---

## 🔹 Version 1 – Basic RAG Implementation

### Retriever.py

- Document loading using `DirectoryLoader` and `Docx2txtLoader`
- Chunking using `RecursiveCharacterTextSplitter`
  - Chunk size: 800
  - Overlap: 100
- Embeddings using HuggingFace model: `BAAI/bge-large-en`
- Vector store using FAISS
- Retriever configuration: `k = 4`
- LLM: ChatGroq with `llama-3.3-70b-versatile`
  - Temperature = 0
- PromptTemplate for response generation
- RetrievalQA chain (`chain_type = "stuff"`)

---

### main.py (FastAPI Backend)

- Loads QA chain
- API endpoint to invoke response
- Returns answer with sources
- Health check endpoint

---

### app.py (Streamlit Frontend)

- UI connected to FastAPI backend
- Session state for conversation persistence
- Displays answer + source documents

---

## 🔹 Version 2 – Hybrid Retrieval

Improvements introduced:

- Replaced FAISS with **ChromaDB**
- Dense Retriever:
  - `k = 3`
  - Score threshold = `0.75`
- BM25 Retriever:
  - `k = 2`
- Hybrid Retrieval:
  - 0.6 weight for Dense
  - 0.4 weight for BM25
- LLM `max_tokens` set to 1024
- Policy router implemented in `main.py`

**Impact:**
- Improved retrieval precision
- Reduced hallucinations
- Better filtering of irrelevant chunks

---

## 🔹 Version 3 – Optimized Production-Ready RAG

### 📊 evaluation.py
Logs:
- Timestamp
- User query
- Retrieved policies
- Unique policies
- Total chunks retrieved

### 🧠 memory.py
Stores:
- Employee ID
- Query history
- Responses

### 🔁 query_rewriter.py
- LLM-based query optimization
- Improves retrieval recall

### 🏆 reranker.py
- Cross-encoder reranking
- Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Improves semantic precision

### 🔀 router.py
Routes queries into:
- Sensitive
- Comparison
- Calculation
- Policy lookup

### Retrieval Tuning
- Dense Retriever:
  - `k = 6`
  - Score threshold = `0.65`
- BM25 Retriever:
  - `k = 3`
- LLM `max_tokens` reduced to 512
- Tone adaptation based on query type

**Impact:**
- Higher precision retrieval
- Better token efficiency
- Improved response grounding
- Enhanced user experience

---

# 🧠 LLMOps Implementation (LangSmith)

Full LLM observability integrated using LangSmith.

## ✅ Project Tracking
- Enabled tracing using LangChain API key
- All LLM runs tracked

## ✅ Component-Level Monitoring
Tracked:
- ChatGroq response runs
- Query rewriting runs
- Retrieval runs
- Reranking runs

## ✅ Evaluators Implemented
- Latency risk monitoring
- Hallucination detection
- Retrieval quality scoring

## 🚨 Alerts Configured
- Latency Alert: > 1.8 seconds
- Error Count Alert: > 1

## 📊 Metrics Monitored
- P50 and P99 latency
- Token usage trends
- Error rates
- Run-level breakdown
- Dashboard insights

This transforms the chatbot into a monitored, production-style LLM system.

---

# 📈 System Capabilities

✔ Hybrid RAG architecture  
✔ Query rewriting  
✔ Cross-encoder reranking  
✔ Intent-based routing  
✔ Tone adaptation  
✔ Memory support  
✔ Structured API responses  
✔ Token usage optimization  
✔ Latency monitoring  
✔ Production-grade observability  

---

# 🧪 How to Run Locally

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt

2️⃣ Set Environment Variables
GROQ_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=HR-RAG-Chatbot
CHROMA_PATH=./chroma_db
3️⃣ Start Backend
python main.py

Access:

http://127.0.0.1:8000/docs
🏗️ Deployment Ready

Designed for deployment on:

Google Cloud Run

Railway

Azure Container Apps

Supports:

Docker containerization

Environment variable configuration

Cloud port binding

🎯 Key Learnings

Building scalable RAG systems

Hybrid retrieval strategies

Query rewriting for recall improvement

Cross-encoder reranking for precision

Token & latency optimization

Implementing LLM observability

Monitoring P50 vs P99 performance metrics

Production mindset for AI applications

🧠 Interview Highlights

This project demonstrates:

End-to-end RAG architecture design

Retrieval optimization techniques

Reranking strategies

Intent routing logic

Token & latency monitoring

Real-world LLMOps practices

Production-ready AI system thinking

