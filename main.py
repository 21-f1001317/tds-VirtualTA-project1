from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dummy_embedder import DummyEmbeddings
import os

app = FastAPI()

# Allow frontend or curl to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Chroma DB (already created)
embedding = DummyEmbeddings()
db = Chroma(persist_directory="chroma", embedding_function=embedding)

# Define input model
class Query(BaseModel):
    question: str
    image: str | None = None

@app.post("/api/")
async def query_api(query: Query):
    question = query.question.strip()
    
    # Search for top result
    results = db.similarity_search(question, k=1)
    
    if not results:
        return {"answer": "No relevant answer found."}
    
    top_doc: Document = results[0]
    return {
        "answer": top_doc.page_content,
        "source": top_doc.metadata.get("source", "unknown")
    }
