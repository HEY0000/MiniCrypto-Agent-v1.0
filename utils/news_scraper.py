# utils/news_scraper.py
import feedparser

def get_rss_news(feed_url="https://cointelegraph.com/rss"):
    feed = feedparser.parse(feed_url)
    return [
        {"title": entry.title, "link": entry.link, "summary": entry.summary}
        for entry in feed.entries
    ]

# test
if __name__ == "__main__":
    news = get_rss_news()
    for n in news[:5]:
        print(n["title"])
