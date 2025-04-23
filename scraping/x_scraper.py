import os
import tweepy
from dotenv import load_dotenv
from datetime import datetime

class TwitterScraper:
    def __init__(self):
        load_dotenv()
        self.authenticate()

    def authenticate(self):
        try:
            # Retrieve Twitter API credentials from environment variables
            bearer_token = os.getenv("BEARER_TOKEN")
            if not bearer_token:
                raise ValueError("Bearer token not found in environment variables.")
            
            # Initialize the Tweepy client with the bearer token
            self.client = tweepy.Client(bearer_token=bearer_token)
            print("Authentication successful.")
        except Exception as auth_error:
            print(f"Authentication failed: {auth_error}")
            self.client = None


    def fetch_tweets(self, user_handle, limit=10):
        if not self.client:
            print("Client is not authenticated. Cannot fetch tweets.")
            return []

        query = f'from:{user_handle} has:links -is:retweet'

        try:
            print(f"\nFetching tweets at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            tweets = self.client.search_recent_tweets(
                query=query,
                tweet_fields=['context_annotations', 'created_at'],
                max_results=limit
            )
            if tweets.data:
                return [{
                    'post_date': tweet.created_at,
                    'content': tweet.text,
                    'user_handle': user_handle,
                    'source': 'twitter',
                    'stock_related': False,         # Can be enhanced with logic later
                    'stock_name': 'N/A',            # Can extract from context_annotations if needed
                    'influence': None               # Optional: NLP logic could populate this
                } for tweet in tweets.data]
            else:
                print("No tweets found.")
                return []
        except tweepy.TweepyException as api_error:
            print(f"Error fetching tweets: {api_error}")
            return []
