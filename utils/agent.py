# utils/agent.py
import os
from openai import OpenAI
from utils.gpt_helper import extract_coin_name, summarize_content
from utils.news_scraper import get_rss_news
from utils.tweet_scraper import get_recent_tweets
from utils.price_fetcher import get_price

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    base_url="https://api.openai.com/v1"
)

def coin_advisor_agent(user_input: str) -> str:
    try:
        coin = extract_coin_name(user_input)
        if coin == "None":
            return "문장에서 코인 이름을 찾을 수 없어요 😥"

        price_info = get_price(coin)
        if not price_info["price"]:
            return f"{coin}의 가격 정보를 찾을 수 없어요."

        news_titles = [n['title'] for n in get_rss_news()]
        news_summary = summarize_content(news_titles, label="뉴스")

        tweets = get_recent_tweets(query=coin.split("-")[0].lower())
        tweet_summary = summarize_content(tweets, label="트윗")

        final_prompt = f"""
        사용자의 질문: "{user_input}"
        현재 코인: {coin}
        시세: ${price_info['price']}
        최근 뉴스 요약: {news_summary}
        최근 트윗 요약: {tweet_summary}

        위 정보를 바탕으로 초보자가 지금 이 코인을 매수해도 괜찮을지 친절하게 알려줘.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI 에이전트 처리 중 오류가 발생했어요: {e}"
