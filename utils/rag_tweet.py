from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

TWEET_INDEX_PATH = "faiss_tweet_index"

def build_tweet_index(tweet_texts, save_path=TWEET_INDEX_PATH):
    docs = [Document(page_content=t) for t in tweet_texts]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(save_path)

def answer_tweet_query(user_query, index_path=TWEET_INDEX_PATH):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_type="similarity", k=3)
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4"),
        retriever=retriever
    )
    return qa_chain.run(user_query)