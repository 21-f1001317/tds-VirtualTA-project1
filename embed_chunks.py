import os
import json
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
from dummy_embedder import DummyEmbeddings

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Set OpenAI API credentials for LangChain
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")

# ✅ Load chunked data
print("📂 Loading chunks.json...")
with open("chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

# ✅ Convert to LangChain Documents
print(f"📄 Preparing {len(chunks)} chunks...")
docs = [Document(page_content=chunk["text"], metadata={"source": chunk["source"]}) for chunk in chunks]

# ✅ Embed and store in Chroma DB
print("🚀 Embedding documents...")

# embedding = OpenAIEmbeddings()
embedding = DummyEmbeddings()

persist_dir = "chroma"

db = Chroma(
    embedding_function=embedding,
    persist_directory=persist_dir
)
db.add_documents(docs)
db.persist()
print("✅ Embedding complete! Chroma DB saved to /chroma")
