from dotenv import load_dotenv
import os
from scraping.truth_scraper import TruthScraper
from scraping.x_scraper import TwitterScraper
from db.db_operations import Database
import pandas as pd

# Load environment variables from the .env file
load_dotenv()
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

def main():
    while True:
        mode = input("Enter source (x / truth / csv) or 'exit' to quit: ").strip().lower()
        if mode == 'x':
            x()
        elif mode == 'truth':
            truth()
        elif mode == 'csv':
            load_from_csv()
        elif mode == 'exit':
            print("Exiting...")
            break
        else:
            break
            print("Invalid input. Please enter 'x', 'truth', 'csv' or 'exit'.")




def truth():
    print(f'truth brush')
    # Retrieve credentials and database connection details from environment variables
    truthsocial_username = os.getenv('TRUTHSOCIAL_USERNAME')
    truthsocial_password = os.getenv('TRUTHSOCIAL_PASSWORD')
    user_handle = 'realDonaldTrump'
    scraper = TruthScraper(truthsocial_username, truthsocial_password)
    posts = scraper.fetch_posts(user_handle)
    if posts:
        trump_db = Database('trump')
        latest_post = posts[0]
        trump_db.insert_post(latest_post)
        trump_db.close()
    # Process the fetched tweets as needed
    for post in posts:
        print(f"Date: {post['created_at']}, post: {post['content']}")


def x():
    print(f'twitter')
    twitter_scraper = TwitterScraper()
    elon_tweets = twitter_scraper.fetch_tweets(user_handle='elonmusk', limit=10)
    if elon_tweets:
        elon_db = Database('elon')
        latest_tweet = elon_tweets[0]
        elon_db.insert_post(latest_tweet)
        elon_db.close()
        # Process the fetched tweets as needed
        for tweet in elon_tweets:
            print(f"Date: {tweet['post_date']}, Tweet: {tweet['content']}")
        
def load_from_csv():
    print("Loading tweets from CSV...")
    try:
        df = pd.read_csv('tweets.csv')
        df.columns = df.columns.str.strip() 
        print(df.head())
        print(f"Columns: {list(df.columns)}")
        elon_db = Database('elon')
        for _, row in df.iterrows():
            date = row.get('created_at')
            print(f'print date:  { date } ')
            print("Row keys:", row.keys())
            #print(row)
            post = {
                'post_date': date,
                'content': row.get('text'),
                'user_handle': 'elonmusk',
                'source': 'twitter',
                'stock_related': False,
                'stock_name': 'N/A',
                'influence': None
            }
            elon_db.insert_post(post)
        elon_db.close()
        print("All tweets inserted from CSV.")
    except Exception as e:
        print(f"Error loading from CSV: {e}")

if __name__ == "__main__":
    main()

