# retriever.py

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from reranker import rerank_documents
from router import route_query
from query_rewriter import rewrite_query
from evaluation import evaluate_retrieval


# ==================================================
# Config
# ==================================================

DATA_PATH = "data"
CHROMA_PATH = "./chroma_db"


# ==========================================
# GLOBAL LOAD (ONLY ONCE)
# ==========================================

print("🚀 Loading Embeddings...")
embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en"
)

print("📦 Loading Chroma Vectorstore...")
vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding
)

print("🔍 Preparing Hybrid Retriever...")

dense_retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.65,
        "k": 6  # reduced from 8 for speed
    }
)

# Load all docs once for BM25
all_docs = vectorstore.get()

documents = [
    Document(page_content=text, metadata=meta)
    for text, meta in zip(all_docs["documents"], all_docs["metadatas"])
]

bm25 = BM25Retriever.from_documents(documents)
bm25.k = 3

hybrid_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, bm25],
    weights=[0.6, 0.4]
)

print("✅ Retriever Ready!")


# ==========================================
# VECTORSTORE CREATION (RUN ONCE)
# ==========================================

def create_vectorstore():

    loader = DirectoryLoader(
        path=DATA_PATH,
        glob="**/*.docx",
        loader_cls=Docx2txtLoader
    )

    documents = loader.load()

    if not documents:
        print("❌ No documents found in data folder")
        return

    processed_docs = []

    for doc in documents:
        file_name = os.path.basename(doc.metadata["source"])
        policy_name = file_name.replace(".docx", "")

        processed_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={
                    "policy_name": policy_name,
                    "company": "A1B2C3 Pvt Ltd"
                }
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    split_docs = splitter.split_documents(processed_docs)

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding,
        persist_directory=CHROMA_PATH
    )

    vectorstore.persist()

    print("✅ Chroma Vectorstore Created Successfully")


# ==========================================
# MAIN RAG PIPELINE
# ==========================================

def generate_answer(query):

    # 1️⃣ Route Intent
    route_type = route_query(query)

    if route_type == "clarification_needed":
        return "Could you please clarify your HR query?", []

    # 2️⃣ Conditional Rewrite
    if route_type in ["policy_lookup", "comparison"]:
        query = rewrite_query(query)

    # 3️⃣ Hybrid Retrieval (FAST - no reload)
    retrieved_docs = hybrid_retriever.invoke(query)

    # 4️⃣ Light Reranking (Reduced Top-K)
    reranked_docs = rerank_documents(query, retrieved_docs, top_k=2)

    # 5️⃣ Evaluation Logging
    evaluate_retrieval(query, reranked_docs)

    # 6️⃣ Tone Adaptation
    tone_instruction = ""

    if route_type == "sensitive":
        tone_instruction = "Respond in a supportive and professional HR tone."

    elif route_type == "comparison":
        tone_instruction = "Provide a structured comparison using bullet points."

    elif route_type == "calculation":
        tone_instruction = "Explain the calculation clearly step by step."

    # 7️⃣ Prepare Context
    context = "\n\n".join([doc.page_content for doc in reranked_docs])

    # 8️⃣ LLM Call (Fast)
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=512  # reduced from 1024 for speed
    )

    prompt = f"""
You are an official HR assistant for A1B2C3 Pvt Ltd.

{tone_instruction}

Use ONLY the provided context to answer.

If context is completely irrelevant or empty, say:
"I could not find this information in company policies."

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return response.content, reranked_docs


# ==========================================
# RUN INGESTION MANUALLY
# ==========================================

if __name__ == "__main__":
    create_vectorstore()