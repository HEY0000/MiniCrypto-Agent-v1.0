# main.py

import streamlit as st
from utils.gpt_helper import extract_coin_name, summarize_content, summarize_technical_indicators
from utils.news_scraper import get_rss_news
from utils.tweet_scraper import get_recent_tweets
from utils.price_fetcher import get_price
from utils.agent import coin_advisor_agent
from utils.chart_generator import plot_candlestick_with_indicators
from utils.rag_news import build_news_index, answer_news_query

st.set_page_config(page_title="코린이 AI 코인 쇼핑 도우미", page_icon="🪙")
st.title("🪙 코린이 AI 코인 쇼핑 도우미")
st.write("AI가 뉴스와 트윗을 요약하고, 시세와 함께 매수 판단까지 도와줍니다!")

# ✅ 모드 선택
mode = st.radio("모드 선택", ["AI 요약 도우미 (분리형)", "AI 조언 에이전트 (통합형)"])

interval_options = {
    "일봉 (1d)": "1d",
    "주봉 (1wk)": "1wk",
    "월봉 (1mo)": "1mo"
}
chart_interval_label = st.selectbox("캔들차트 기간 선택", list(interval_options.keys()))
chart_interval = interval_options[chart_interval_label]

# ✅ 사용자 입력
query = st.text_input("궁금한 코인을 입력하세요 (예: bitcoin, ethereum)")

if query:
    if mode == "AI 요약 도우미 (분리형)":
        # ✅ 코인 시세
        try:
            coin_ticker = extract_coin_name(query)
            if coin_ticker != "None":
                price_info = get_price(coin_ticker)
                if price_info["price"]:
                    st.metric(f"📈 {coin_ticker} 가격", f"${price_info['price']}", help=price_info["time"])
        except Exception as e:
            st.error(f"코인명 추출 실패: {e}")

        # ✅ 뉴스 RAG 요약
        st.subheader("📰 뉴스 RAG 요약")
        try:
            news_list = get_rss_news()
            news_texts = []
            for n in news_list:
                title = n.get("title", "")
                desc = n.get("summary", "") or n.get("description", "")
                content = f"{title}. {desc}".strip()
                if content:
                    news_texts.append(content)

            if not news_texts:
                raise ValueError("🔍 뉴스 내용이 비어 있어 인덱스를 생성할 수 없습니다.")

            build_news_index(news_texts, save_path="faiss_news_index")
            rag_answer = answer_news_query(query, index_path="faiss_news_index")
        

            st.write("📚 GPT 요약:")
            st.write(summarize_content([n["title"] for n in news_list], label="뉴스"))
            # st.write("🔍 RAG 기반 응답:")
            # st.write(rag_answer.encode("utf-8", "ignore").decode("utf-8"))
            st.markdown("🔍 **RAG 기반 응답:**")

            # 긴 응답을 나눠서 출력
            for line in rag_answer.strip().split("\n"):
                st.markdown(line)

        except Exception as e:
            st.error(f"뉴스 RAG 요약 실패: {e}")

        # ✅ 트윗 요약
        st.subheader("🐦 트위터 요약")
        try:
            tweet_list = get_recent_tweets(query=query, max_results=10)
            tweet_texts = [t for t in tweet_list if isinstance(t, str)]
            tweet_summary = summarize_content(tweet_texts, label="트윗")
            st.write(tweet_summary)
        except Exception as e:
            st.error(f"트윗 요약 실패: {e}")

    elif mode == "AI 조언 에이전트 (통합형)":
        st.subheader("💡 AI의 조언")
        try:
            coin_name = extract_coin_name(query)
            if coin_name == "None":
                st.warning("❗ 문장에서 코인 이름을 찾을 수 없어요.")
                coin_name = None
            elif "-" not in coin_name:
                st.warning(f"⚠️ GPT가 추출한 '{coin_name}'은 yfinance 형식이 아닐 수 있어요.")
        except Exception as e:
            st.error(f"코인명 추출 실패: {e}")
            coin_name = None

        if coin_name:
            with st.spinner("AI가 정보를 분석 중입니다..."):
                try:
                    result = coin_advisor_agent(query)
                    st.write(result)
                except Exception as e:
                    st.error(f"AI 판단 실패: {e}")

            # ✅ 차트 분석
            with st.spinner("📊 차트를 불러오는 중입니다..."):
                period = "3mo" if chart_interval == "1d" else ("1y" if chart_interval == "1wk" else "5y")
                fig, latest_row = plot_candlestick_with_indicators(
                    ticker=coin_name,
                    interval=chart_interval,
                    period=period
                )

                if fig:
                    st.subheader(f"📊 캔들차트 ({chart_interval})")
                    st.pyplot(fig)

                    st.subheader("🤖 차트 해석")
                    try:
                        summary = summarize_technical_indicators(latest_row, coin_name)
                        st.write(summary)
                    except Exception as e:
                        st.error(f"차트 해석 실패: {e}")
                else:
                    st.error("📉 유효한 차트 데이터가 없습니다.")
