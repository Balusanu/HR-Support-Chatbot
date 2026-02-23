# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from retriever import generate_answer, create_vectorstore

import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# Request Model
# ==========================

class ChatRequest(BaseModel):
    question: str


# ==========================
# Startup
# ==========================

@app.on_event("startup")
def startup_event():

    if not os.path.exists("./chroma_db"):
        print("Creating vectorstore...")
        create_vectorstore()
    else:
        print("✅ Chroma DB found.")


# ==========================
# Health Check
# ==========================

@app.get("/health")
def health():
    return {"status": "Running 🚀"}


# ==========================
# Chat Endpoint
# ==========================

@app.post("/chat")
def chat(request: ChatRequest):

    try:
        answer, docs = generate_answer(request.question)

        sources = [
            {
                "policy_name": doc.metadata.get("policy_name"),
                "preview": doc.page_content[:200]
            }
            for doc in docs
        ]

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "HR Support RAG Backend is Live 🚀"}