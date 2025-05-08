# utils/tweet_scraper.py
import tweepy
import os
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    raise ValueError("TWITTER_BEARER_TOKEN not set. Please set it in your ~/.bashrc")

client = tweepy.Client(bearer_token=bearer_token)


def get_recent_tweets(query="bitcoin", max_results=10):
    try:
        tweets = client.search_recent_tweets(query=query, max_results=max_results)
        if tweets.data:
            return [tweet.text for tweet in tweets.data]
        else:
            return ["No tweets found."]
    except tweepy.TooManyRequests:
        return ["Rate limit exceeded. Try again in 15 minutes."]
# test
if __name__ == "__main__":
    for t in get_recent_tweets():
        print(t)
