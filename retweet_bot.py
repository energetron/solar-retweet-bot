import tweepy
import random
import time
import os
from datetime import datetime

# Twitter API credentials
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Broader solar energy keywords
SOLAR_KEYWORDS = [
    'solar', 'SolarEnergy', 'SolarPower', 'RenewableEnergy', 
    'solar energy', 'solar panels', 'clean energy',
    'photovoltaic', 'sun power', 'renewable', 'solar panel',
    'climate change', 'green energy', 'clean power'
]

# Specific solar accounts (without @)
SOLAR_ACCOUNTS = [
    'SolarEnergyUK', 'IRENA', 'Solar_Edition',
    'SolarPowerWorld', 'SEIA', 'SolarQuarter'
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
    # 60% chance to search by keyword, 40% to search by account
    if random.random() < 0.6:
        return random.choice(SOLAR_KEYWORDS)
    else:
        account = random.choice(SOLAR_ACCOUNTS)
        return f"from:{account}"

def should_retweet():
    # 90% chance to retweet when a tweet is found (increased from 80%)
    return random.random() < 0.9

def run_retweet_bot():
    try:
        client = setup_twitter_api()
        
        search_term = get_random_search_term()
        print(f"🔍 Searching for: {search_term}")
        
        # Search for recent tweets (broader search)
        tweets = client.search_recent_tweets(
            query=search_term + " -is:retweet -is:reply",
            max_results=15,  # Increased from 10
            tweet_fields=['author_id', 'created_at', 'public_metrics']
        )
        
        if tweets.data:
            print(f"✅ Found {len(tweets.data)} tweets")
            
            # Filter tweets and pick one randomly
            valid_tweets = [tweet for tweet in tweets.data if should_retweet()]
            
            if valid_tweets:
                tweet_to_retweet = random.choice(valid_tweets)
                
                # Retweet the selected tweet
                client.retweet(tweet_to_retweet.id)
                print(f"🔄 RETWEETED tweet ID: {tweet_to_retweet.id}")
                print(f"📝 Search term: {search_term}")
                print(f"⏰ Time: {datetime.now()}")
                print(f"📊 Tweet stats: {tweet_to_retweet.public_metrics}")
            else:
                print("🤔 Found tweets but decided not to retweet any")
        else:
            print("❌ No tweets found for the search term")
            
    except Exception as e:
        print(f"🚨 Error: {str(e)}")

if __name__ == "__main__":
    run_retweet_bot()
