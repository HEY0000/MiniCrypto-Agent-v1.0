# utils/news_scraper.py
import feedparser

def get_rss_news(feed_url="https://cointelegraph.com/rss"):
    feed = feedparser.parse(feed_url)
    return [
        {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "content": f"{entry.title}. {entry.summary}"  # ✅ 반드시 포함!
        }
        for entry in feed.entries
    ]
# test
if __name__ == "__main__":
    # news = get_rss_news()
    # for n in news[:5]:
    #     print(n["title"])

    news_list = get_rss_news()
    print(f"뉴스 개수: {len(news_list)}")
    for n in news_list[:3]:
        print(n)
