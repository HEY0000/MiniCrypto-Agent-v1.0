# utils/gpt_helper.py
import os
from openai import OpenAI

from langchain.chains import RetrievalQA
from utils.rag_pipeline import load_faiss_index  # 상대 경로로 수정 필요 시 조정
from langchain_community.chat_models import ChatOpenAI


def answer_with_rag(user_query, index_path="faiss_index"):
    vectorstore = load_faiss_index(index_path)
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4"),
        retriever=retriever
    )
    return qa_chain.run(user_query)


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    base_url="https://api.openai.com/v1"
)

COIN_PROMPT_TEMPLATE = """
아래 문장에서 언급된 암호화폐 이름을 yfinance에서 사용하는 형식으로 하나만 반환해줘.
예: bitcoin → BTC-USD, ethereum → ETH-USD, solana → SOL-USD
정확한 심볼이 없으면 영어 이름만 간단히 반환해줘. 정말 없으면 "None"이라고만 답해.
문장: "{user_input}"
"""

def extract_coin_name(user_input: str) -> str:
    prompt = COIN_PROMPT_TEMPLATE.format(user_input=user_input)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def summarize_content(text_list, label="뉴스"):
    if not text_list:
        return "내용이 없습니다."
    
    content = "\n\n".join(text_list[:5])
    prompt = f"""
    다음은 {label} 데이터입니다. 초보자도 이해할 수 있도록 핵심만 간단하게 요약해줘:

    {content}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or gpt-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()


def summarize_technical_indicators(latest_row, coin_name):
    values = latest_row.iloc[0]
    prompt = f"""
    아래는 {coin_name}의 최신 기술 지표입니다:

    - 종가: {values['Close']:.2f}
    - 5일 이동평균: {values['MA5']:.2f}
    - 20일 이동평균: {values['MA20']:.2f}
    - RSI(14): {values['RSI']:.2f}
    - MACD: {values['MACD']:.2f}, Signal: {values['MACDSignal']:.2f}
    - 골든크로스 발생: {'Yes' if values['golden_cross'] else 'No'}

    초보자도 이해할 수 있게 지금 매수 적기인지 간단히 설명해줘.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()
