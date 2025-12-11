import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    # Create a directory for the browser profile to make it persistent
    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    
    print(f"Launching browser with persistent profile at: {user_data_dir}")
    print("This helps avoid detection by Twitter.")
    
    async with async_playwright() as p:
        # Launch persistent context
        # This saves your session, so next time you open it, you might already be logged in
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # args to make it look less like a bot
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--start-maximized"
            ]
        )
        
        page = context.pages[0]
        
        print("Navigating to X.com login page...")
        await page.goto("https://x.com/i/flow/login")
        
        print("\n" + "="*50)
        print("ACTION REQUIRED: Please log in to X (Twitter) in the browser window.")
        print("If you get an error, try refreshing the page or waiting a moment.")
        print("Once you are logged in and see your timeline (Home), come back here.")
        print("="*50 + "\n")
        
        # Wait for user input instead of auto-detecting URL
        input(">>> PRESS ENTER HERE ONCE YOU ARE LOGGED IN <<<")
        
        print("Saving cookies...")
        try:
            # Get cookies from the browser context
            cookies = await context.cookies()
            
            # Convert to the format Twikit expects (dictionary of name: value)
            cookie_dict = {c['name']: c['value'] for c in cookies}
            
            output_path = "twitter_cookies.json"
            with open(output_path, "w") as f:
                json.dump(cookie_dict, f, indent=2)
                
            print(f"✅ Success! Cookies saved to {os.path.abspath(output_path)}")
            print(f"   Saved {len(cookie_dict)} cookies.")
            
        except Exception as e:
            print(f"❌ Failed to save cookies: {e}")
        
        print("Closing browser...")
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
