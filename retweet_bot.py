import tweepy
import random
import time
import os
from datetime import datetime

# Twitter API credentials - will be set automatically
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Solar energy keywords to search for
SOLAR_KEYWORDS = [
    '#SolarEnergy', '#SolarPower', '#RenewableEnergy', 
    'solar energy', 'solar panels', 'solar technology',
    'clean energy', 'photovoltaic'
]

# Specific solar accounts (without @)
SOLAR_ACCOUNTS = [
    'SolarEnergyUK', 'IRENAsolar', 'Solar_Edition',
    'SolarPowerWorld', 'SEIA'
]

def setup_twitter_api():
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    return client

def get_random_search_term():
    # 70% chance to search by keyword, 30% to search by account
    if random.random() < 0.7:
        return random.choice(SOLAR_KEYWORDS)
    else:
        account = random.choice(SOLAR_ACCOUNTS)
        return f"from:{account}"

def should_retweet():
    # 80% chance to retweet when a tweet is found
    return random.random() < 0.8

def run_retweet_bot():
    try:
        client = setup_twitter_api()
        
        search_term = get_random_search_term()
        print(f"Searching for: {search_term}")
        
        # Search for recent tweets
        tweets = client.search_recent_tweets(
            query=search_term + " -is:retweet",
            max_results=10,
            tweet_fields=['author_id', 'created_at']
        )
        
        if tweets.data:
            # Filter tweets and pick one randomly
            valid_tweets = [tweet for tweet in tweets.data if should_retweet()]
            if valid_tweets:
                tweet_to_retweet = random.choice(valid_tweets)
                
                # Retweet the selected tweet
                client.retweet(tweet_to_retweet.id)
                print(f"✅ Retweeted tweet ID: {tweet_to_retweet.id}")
                print(f"🔍 Search term used: {search_term}")
                print(f"⏰ Time: {datetime.now()}")
            else:
                print("🤔 No tweets selected for retweeting this time")
        else:
            print("❌ No tweets found for the search term")
            
    except Exception as e:
        print(f"🚨 Error: {str(e)}")

if __name__ == "__main__":
    run_retweet_bot()
