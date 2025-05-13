# utils/rag_pipeline.py

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.documents import Document
import os

def build_faiss_index(texts, save_path="faiss_index"):
    docs = [Document(page_content=t) for t in texts]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    vectorstore.save_local(save_path)

def load_faiss_index(path="faiss_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
