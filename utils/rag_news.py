# utils/rag_news.py

from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os

NEWS_INDEX_PATH = "faiss_news_index"

def build_news_index(news_texts, save_path=NEWS_INDEX_PATH):
    """
    뉴스 본문 또는 타이틀+설명 리스트를 받아 FAISS 인덱스를 생성합니다.
    """
    if not news_texts:
        raise ValueError("🔍 뉴스 내용이 비어 있어 인덱스를 생성할 수 없습니다.")

    docs = [Document(page_content=t.strip()) for t in news_texts if t.strip()]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(save_path)


def answer_news_query(user_query, index_path=NEWS_INDEX_PATH):
    """
    사용자 질문에 대해 FAISS에서 유사한 뉴스 벡터를 검색하여 GPT로 응답합니다.
    """
    embeddings = OpenAIEmbeddings()

    # 안전한 로딩 (자신이 만든 인덱스라면 괜찮음)
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_type="similarity", k=3)
    qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=retriever,
    return_source_documents=False

)

    # 📢 프롬프트 개선 (뉴스는 과거 정보라는 점 안내)
    prompt = f"""아래는 과거 뉴스입니다. 그래도 관련 내용이 있다면 요약해서 알려주세요.
질문: {user_query}
"""
    return qa_chain.run(prompt)
