# main.py

import streamlit as st
from utils.gpt_helper import extract_coin_name, summarize_content
from utils.news_scraper import get_rss_news
from utils.tweet_scraper import get_recent_tweets
from utils.price_fetcher import get_price   # ← 여기에 import



st.set_page_config(page_title="코린이 AI 코인 도우미", page_icon="🪙")
st.title("🪙 코린이 AI 코인 쇼핑 도우미")

# ✅ BTC 실시간 가격 표시
price_info = get_price("BTC-USD")
if price_info["price"]:
    st.metric("📈 BTC 가격", f"${price_info['price']}", help=price_info["time"])

st.write("뉴스와 트윗을 한눈에! 차트도 곧 들어옵니다 👀")



# 사용자 입력
query = st.text_input("궁금한 코인을 입력하세요 (예: bitcoin, ethereum)")

if query:
    # 🔍 GPT로 코인명 추출
    try:
        coin_ticker = extract_coin_name(query)
        if coin_ticker != "None":
            price_info = get_price(coin_ticker)
            if price_info["price"]:
                st.metric(f"📈 {coin_ticker} 가격", f"${price_info['price']}", help=price_info["time"])
    except Exception as e:
        st.error(f"코인명 추출 실패: {e}")

    # 📰 뉴스 요약
    st.subheader("📰 뉴스 요약")
    try:
        news_list = get_rss_news()
        news_titles = [n["title"] for n in news_list]
        news_summary = summarize_content(news_titles, label="뉴스")
        st.write(news_summary)
    except Exception as e:
        st.error(f"뉴스 요약 실패: {e}")

    # 🐦 트윗 요약
    st.subheader("🐦 트위터 요약")
    try:
        tweet_list = get_recent_tweets(query=query, max_results=10)
        tweet_texts = [t for t in tweet_list if isinstance(t, str)]
        tweet_summary = summarize_content(tweet_texts, label="트윗")
        st.write(tweet_summary)
    except Exception as e:
        st.error(f"트윗 요약 실패: {e}")
