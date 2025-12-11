import asyncio
import os
import json
from twikit import Client  # pyright: ignore[reportMissingImports]

async def test_twikit():
    print("Testing Twikit Login...")
    
    # Initialize client
    client = Client('en-US')
    
    # Load credentials from environment or use provided ones (placeholder)
    # In real usage, load from .env
    # Try to load from .env file manually if not already loaded
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
    except:
        pass

    USERNAME = os.getenv("TWITTER_USERNAME", "your_username")
    EMAIL = os.getenv("TWITTER_EMAIL", "your_email")
    PASSWORD = os.getenv("TWITTER_PASSWORD", "your_password")
    COOKIES_PATH = "twitter_cookies.json"

    try:
        # Check if cookies exist to avoid login
        if os.path.exists(COOKIES_PATH):
            print("Loading cookies...")
            client.load_cookies(COOKIES_PATH)
        else:
            print("Logging in...")
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD
            )
            client.save_cookies(COOKIES_PATH)
            print("Login successful and cookies saved.")

        # Test fetching a user
        target_user = "elonmusk" 
        print(f"Fetching profile for @{target_user}...")
        user = await client.get_user_by_screen_name(target_user)
        
        print(f"Name: {user.name}")
        print(f"Followers: {user.followers_count}")
        print(f"Description: {user.description}")
        
        # Test fetching latest tweets
        print(f"\nFetching latest tweets from @{target_user}...")
        tweets = await user.get_tweets('Tweets', count=5)
        
        for tweet in tweets:
            print(f"- [{tweet.created_at}] {tweet.text[:50]}... (Likes: {tweet.favorite_count})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_twikit())
