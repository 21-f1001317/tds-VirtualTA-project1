from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from langchain.schema import Document
import json

os.environ["OPENAI_API_BASE"] = "https://ai.iitm.ac.in/proxy/v1"
load_dotenv()
with open("chunks.json") as f:
    chunks = json.load(f)

docs = [Document(page_content=c["text"], metadata={"source": c["source"]}) for c in chunks]
db = Chroma.from_documents(docs, OpenAIEmbeddings(), persist_directory="chroma")
db.persist()
