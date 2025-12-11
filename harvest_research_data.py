import asyncio
import os
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, LLMConfig, VirtualScrollConfig, DefaultTableExtraction, LinkPreviewConfig, MemoryAdaptiveDispatcher, CrawlerMonitor, DisplayMode, RateLimiter
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DFSDeepCrawlStrategy # Import DFS strategy
from crawl4ai.deep_crawling import FilterChain, URLPatternFilter, DomainFilter, ContentTypeFilter # Import Deep Crawling Filters
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.content_filter_strategy import PruningContentFilter, LLMContentFilter # Import LLM content filter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy # Import faster scraping strategy
from crawl4ai import RoundRobinProxyStrategy # Import proxy strategy
# LLMTableExtraction might be missing in this version, falling back to standard LLMExtraction
# from crawl4ai.extraction_strategy import LLMTableExtraction 
from crawl4ai.browser_profiler import BrowserProfiler # Import browser profiler for managed profiles
from playwright.async_api import Page, BrowserContext # Import Playwright types for hooks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
try:
    from twikit import Client
except ImportError:
    print("Warning: 'twikit' not installed. Twitter scraping will be skipped. Run 'pip install twikit'")
    Client = None

# Define the schema for a SINGLE user profile
class UserProfile(BaseModel):
    username: Optional[str] = Field(None, description="The username or handle of the user.")
    user_id: Optional[str] = Field(None, description="The unique identifier or ID of the user.")
    wallet_address: Optional[str] = Field(None, description="The on-chain wallet address (e.g., starting with 0x).")
    points_or_score: Optional[str] = Field(None, description="The user's score, points, XP, or reputation.")
    leaderboard_rank: Optional[str] = Field(None, description="The user's rank or position on a leaderboard (e.g., #1, 1st, 50).")
    twitter_handle: Optional[str] = Field(None, description="The user's Twitter/X handle (e.g. @username) if found.")
    twitter_stats: Optional[Dict[str, Any]] = Field(None, description="Scraped Twitter stats: followers, recent_engagement, tournaments, etc.")
    additional_info: Dict[str, Any] = Field({}, description="Any other relevant metrics like level, quests completed, etc.")

# Define the schema for the ENTIRE PAGE result (handling lists)
class PageData(BaseModel):
    users: List[UserProfile] = Field(default_factory=list, description="List of user profiles found on the page.")
    page_summary: Optional[str] = Field(None, description="Brief summary of what this page is (e.g., 'Leaderboard', 'User Profile', 'Quest Page').")

async def main():
    # Manual profile path to avoid Windows asyncio subprocess issues with interactive profiler
    profile_path = os.path.join(os.getcwd(), "chrome_profile")
    os.makedirs(profile_path, exist_ok=True)
    print(f"Using persistent browser profile at: {profile_path}")
    
    # profiler = BrowserProfiler()
    # profiles = profiler.list_profiles()
    # ... (commented out interactive profiler code) ...
    
    print("If you want to access private data, run this script once, manually log in to the sites in the opened browser, and then close it.")

    # Initialize Twitter Client (Twikit)
    twitter_client = None
    if Client:
        try:
            twitter_client = Client('en-US')
            # Attempt to load cookies first
            cookies_path = os.getenv("TWITTER_COOKIES_PATH", "twitter_cookies.json")
            
            if os.path.exists(cookies_path):
                twitter_client.load_cookies(cookies_path)
                print("Loaded Twitter cookies.")
            elif os.getenv("TWITTER_USERNAME") and os.getenv("TWITTER_PASSWORD"):
                print(f"Logging into Twitter as {os.getenv('TWITTER_USERNAME')} via Twikit...")
                await twitter_client.login(
                    auth_info_1=os.getenv("TWITTER_USERNAME"),
                    auth_info_2=os.getenv("TWITTER_EMAIL"),
                    password=os.getenv("TWITTER_PASSWORD")
                )
                twitter_client.save_cookies(cookies_path)
                print("Logged in to Twitter and saved cookies.")
            else:
                print("No Twitter credentials found in environment (TWITTER_USERNAME/PASSWORD).") 
                print("Please check your .env file.")
                twitter_client = None
        except Exception as e:
            print(f"Failed to initialize Twitter client: {e}")
            twitter_client = None

    # 0. Configure Proxy Strategy (Optional)
    # To use proxies, set the PROXIES environment variable:
    # export PROXIES="ip:port:user:pass,ip:port:user:pass"
    proxies = []
    
    # Try loading from .env file (if python-dotenv is installed) or environment
    try:
        from dotenv import load_dotenv
        # Explicitly load the .env file if it exists, or fallback to env_config.txt
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.exists(env_path):
             env_path = os.path.join(os.path.dirname(__file__), 'env_config.txt')
        
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"Loaded environment from {env_path}")
            # Debug: Print loaded keys related to Twitter
            print("Debug: Checking for TWITTER keys in environment...")
            for key in os.environ:
                if "TWITTER" in key:
                    print(f"  Found key: {key}")
        else:
            print("Warning: No .env or env_config.txt file found.")
    except ImportError:
        print("Warning: python-dotenv not installed. Skipping .env load.")

    if os.getenv("PROXIES"):
        try:
            proxy_list = os.getenv("PROXIES").split(",")
            for proxy in proxy_list:
                if proxy.strip():
                    parts = proxy.strip().split(":")
                    if len(parts) == 4:
                        proxies.append({
                            "server": f"http://{parts[0]}:{parts[1]}",
                            "username": parts[2],
                            "password": parts[3]
                        })
                    elif len(parts) == 2:
                         proxies.append(parts[0] + ":" + parts[1]) # Just IP:Port
            print(f"Loaded {len(proxies)} proxies from environment.")
        except Exception as e:
            print(f"Error parsing proxies: {e}")
    else:
        print("No PROXIES environment variable found. Running without proxies.")

    # Note: RoundRobinProxyStrategy in v0.7.7 expects a list of dictionaries or strings?
    # The error "dict object has no attribute server" suggests it might be expecting objects or different dict structure
    # OR the library code is trying to access .server on a dict.
    # Let's try passing simple strings if the complex dict failed, or ensure we are not breaking it.
    # Actually, the traceback shows `next_proxy.server`. This implies `next_proxy` is expected to be an OBJECT with a .server attribute,
    # but `RoundRobinProxyStrategy` returned a DICT. 
    # This is a library bug/mismatch in 0.7.7. 
    # Workaround: Disable proxy strategy for now if it crashes, OR wrap it.
    
    # Given the error, let's disable the proxy strategy to unblock the crawl.
    print("⚠️  Disabling Proxy Strategy due to library version mismatch (dict vs object).")
    proxy_strategy = None 
    # proxy_strategy = RoundRobinProxyStrategy(proxies) if proxies else None

    # List of target URLs to crawl (Entry points)
    urls = [
        "https://kaito.ai/",
        # "https://<yaps-platform>/", 
        "https://wallchain.xyz/",
        "https://galxe.com/",
        "https://layer3.xyz/quests/",
        "https://cookie.fun/quests/",
        "https://cookie3.com/",
        "https://www.xeet.ai/"
    ]

    # 1. Define the LLM Extraction Strategy
    # We use PageData schema to capture multiple users if a leaderboard is present
    llm_strategy = LLMExtractionStrategy(
        # provider="ollama/deepseek-r1", 
        # api_token="no-token", 
        llm_config=LLMConfig(provider="ollama/deepseek-r1", api_token="no-token"),
        schema=PageData.model_json_schema(),
        extraction_type="schema", # Explicitly set extraction type
        input_format="fit_markdown", # Use fit_markdown for better token efficiency with PruningContentFilter
        instruction="""
        Analyze the page content. 
        If it's a leaderboard, extract ALL user rows with their ranks, usernames, scores, and wallet addresses.
        If it's a single user profile, extract their details.
        
        CRITICAL: Look for specific 'Twitter' or 'X' engagement metrics IF displayed. 
        Examples to extract into 'additional_info': 
        - "Twitter Handle" or "Connected X Account"
        - "Tweets: 50" or "X Engagement: 500"
        - "Referral count" or "Invites"
        
        Look specifically for: 'Rank', 'Position', '#', 'Points', 'Score', 'XP', 'Address', 'User'.
        """,
        # extra_args={"temperature": 0}
    )

    # 2. Define Browser Configuration (Persistent Profile)
    # Note: Stealth mode is not compatible with 'builtin' mode. 
    # We prioritize stealth and managed profile over 'builtin' for this harvesting task.
    browser_config = BrowserConfig(
        verbose=True,
        headless=False, # Set to False so you can see the browser and login if needed
        # browser_mode="builtin", # Disabled to allow stealth mode
        use_managed_browser=True, # Enable managed browser for the profile
        user_data_dir=profile_path, # Use the path from BrowserProfiler
        # use_persistent_context=True, # Implicitly true when using managed browser/profile path
        enable_stealth=True, # Enable stealth mode
        viewport_width=1280, # Realistic viewport
        viewport_height=800,
        # Performance optimizations via extra_args instead of browser_args
        extra_args=[
            "--disable-gpu",
            "--disable-dev-shm-usage", 
            "--no-sandbox",
        ]
    )

    # Use AsyncPlaywrightCrawlerStrategy for advanced capabilities if needed,
    # but the standard AsyncWebCrawler with browser_config is often sufficient.
    # To use 'undetected' mode, one would typically use a custom adapter, 
    # but standard persistent profile is usually enough for research gathering.

    # 3. Define Deep Crawl Configuration
    # Use DFS (Depth-First Search) for deep exploration of specific paths (e.g. Quest -> Quest Details -> User)
    # BFS (Breadth-First Search) is better for wide scanning (e.g. Leaderboard -> All Profiles)
    # Let's use BFS as default but configured for depth
    
    # Define Filters to keep the crawl focused
    # This prevents the crawler from wandering into "About Us", "Privacy Policy", or external Twitter links during deep crawl
    deep_crawl_filters = FilterChain([
        # Only crawl URLs that look like they might contain interesting data
        URLPatternFilter(patterns=[
            "*quest*", "*user*", "*profile*", "*leaderboard*", "*stats*", "*score*", 
            "*points*", "*campaign*", "*mission*", "*dashboard*"
        ]),
        # Ensure we stick to relevant content types
        ContentTypeFilter(allowed_types=["text/html"])
    ])

    crawl_config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,             # Increased depth to find more nested data
            include_external=False,  # strictly stay on the same domain
            filter_chain=deep_crawl_filters # Apply the filters defined above
        ),
        # Heuristic Markdown Generation to reduce noise (menus, footers, etc.)
        # Using LLMContentFilter for smarter content filtering (removing navs, sidebars, ads)
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=LLMContentFilter(
                llm_config=LLMConfig(provider="ollama/deepseek-r1", api_token="no-token"),
                instruction="""
                Extract the main content of the page, focusing on user profiles, leaderboards, and quest details.
                Remove navigation menus, footers, sidebars with external links, and advertisements.
                Keep all tables and lists intact.
                """,
                chunk_token_threshold=4096,
                verbose=True
            )
        ),
        # Use LXML scraping strategy for speed and efficiency on large DOMs
        scraping_strategy=LXMLWebScrapingStrategy(),
        extraction_strategy=llm_strategy, 
        cache_mode="bypass",
        fetch_ssl_certificate=True, # Fetch SSL certificate for verification
        proxy_rotation_strategy=proxy_strategy, # Use proxy rotation if configured
        
        # Link Scoring & Preview - Helps identify high-value links to prioritize in deeper crawls
        link_preview_config=LinkPreviewConfig(
            include_internal=True,
            max_links=15, # Analyze top 15 links per page
            concurrency=5, # Parallel processing
            verbose=False,
            # Prioritize links that look like leaderboards, profiles, or quests
            query="leaderboard profile user quest stats ranking score points"
        ),
        score_links=True, # Enable relevance scoring based on the query above
        
        # Capture network traffic - Disabled for stability
        capture_network_requests=False,
        # Capture console messages - Disabled for stability
        capture_console_messages=False,
        
        # Virtual Scroll Configuration for Infinite Scroll Pages (Twitter-like)
        virtual_scroll_config=VirtualScrollConfig(
            scroll_count=20,       # Scroll 20 times (adjust for deeper history)
            scroll_by="container_height", # Smart scroll by visible area
            wait_after_scroll=1.0,  # Wait 1s for content to load
            container_selector="body" # Default selector, can be overridden by specific site configs if needed
        ),
        
        # Table Extraction Strategy - Useful for structured leaderboards that are HTML tables
        # Replaced DefaultTableExtraction with LLMTableExtraction for better handling of complex tables
        table_extraction=DefaultTableExtraction(
            table_score_threshold=6, # Moderate sensitivity
            min_rows=2, # Must have at least 2 rows to be considered a leaderboard
            verbose=True
        ),
        
        # Click 'Show More' buttons if present (still useful for non-virtualized "Load More" buttons)
        js_code=["""
            (async () => {
                const distance = 500;
                const delay = 500;
                const max_scrolls = 20; // Scroll more
                
                // 1. Scroll down to load lazy content
                for(let i=0; i<max_scrolls; i++) {
                    window.scrollBy(0, distance);
                    await new Promise(r => setTimeout(r, delay));
                }

                // 2. Try to click 'Load More' / 'Show More' / 'Next' buttons
                const selectors = [
                    "button:contains('Load More')", 
                    "button:contains('Show More')", 
                    "button:contains('Next')",
                    ".load-more-btn", 
                    "[aria-label='Load more']",
                    "[aria-label='Next page']",
                    ".pagination-next" 
                ];
                
                // Try clicking multiple times if it's a "Load More" button
                for(let i=0; i<5; i++) { 
                    let clicked = false;
                    for(const sel of selectors) {
                        try {
                            const btn = document.querySelector(sel);
                            if(btn && btn.offsetParent !== null) { // Check if visible
                                btn.scrollIntoView();
                                btn.click();
                                await new Promise(r => setTimeout(r, 2000)); // Wait for load
                                clicked = true;
                                break; // Move to next iteration
                            }
                        } catch(e) {}
                    }
                    if(!clicked) break; // If no button found, stop trying
                }
            })();
        """]
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        
        # Define Hooks for advanced interaction
        async def on_page_context_created(page: Page, context: BrowserContext, **kwargs):
            # Set a realistic viewport size just in case
            await page.set_viewport_size({"width": 1280, "height": 800})
            return page

        async def before_goto(page: Page, context: BrowserContext, url: str, **kwargs):
            # Example: Add custom headers if needed (e.g., specific Accept-Language)
            await page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
            return page

        # Register Hooks
        crawler.crawler_strategy.set_hook("on_page_context_created", on_page_context_created)
        crawler.crawler_strategy.set_hook("before_goto", before_goto)

        print(f"=== Starting Deep Crawl for {len(urls)} URLs ===")
        
        # Sequential processing for maximum stability
        results = []
        for url in urls:
            print(f"Processing: {url}")
            try:
                result = await crawler.arun(
                    url=url,
                    config=crawl_config
                )
                results.append(result)
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")

        print(f"\n=== Completed Crawl of {len(results)} URLs ===")
        
        # Data Analysis Phase
        all_users_data = []

        for i, result in enumerate(results):
            url = result.url
            if result.success:
                print(f"Processing result for: {url}")
                page_url = result.url
                safe_name = page_url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
                
                # Save extracted data
                if result.extracted_content:
                    try:
                        # Parse to check if we actually got users
                        data = json.loads(result.extracted_content)
                        
                        current_users = []
                        
                        # Handle cases where data might be a list or a dict
                        if isinstance(data, list):
                            if data:
                                print(f"  [Data] Found {len(data)} items on {page_url}")
                                current_users = data
                            else:
                                print(f"  [Empty List] {page_url}")
                        elif isinstance(data, dict):
                            users_found = data.get("users", [])
                            if users_found:
                                print(f"  [Data] Found {len(users_found)} users on {page_url}")
                                current_users = users_found
                            else:
                                print(f"  [No Users] {page_url} (Summary: {data.get('page_summary', 'N/A')})")
                        else:
                            print(f"  [Unknown Data Type] {page_url}")

                        # Enrich with Twitter Data if Client is available
                        if twitter_client and current_users:
                            print(f"  [Twitter] Enriching {len(current_users)} profiles with Twikit...")
                            for user in current_users:
                                # Find handle
                                handle = user.get('twitter_handle') or user.get('additional_info', {}).get('twitter')
                                
                                if handle:
                                    # Clean handle
                                    if handle.startswith("https://twitter.com/") or handle.startswith("https://x.com/"):
                                        handle = handle.split("/")[-1]
                                    handle = handle.strip("@")
                                    
                                    try:
                                        # Fetch user stats
                                        tw_user = await twitter_client.get_user_by_screen_name(handle)
                                        user['twitter_stats'] = {
                                            "followers": tw_user.followers_count,
                                            "following": tw_user.following_count,
                                            "tweets": tw_user.statuses_count,
                                            "description": tw_user.description,
                                            "verified": tw_user.verified
                                        }
                                        
                                        # Analyze recent tweets for platform relevance
                                        # Try to find tweets mentioning the platform to see if they drove engagement
                                        platform_name = "galxe" if "galxe" in url else "layer3" if "layer3" in url else "cookie" if "cookie" in url else "kaito" if "kaito" in url else ""
                                        
                                        if platform_name:
                                            print(f"    ? Searching tweets for '{platform_name}'...")
                                            # Fetch recent tweets (limit to 10 to be safe)
                                            # Note: get_tweets syntax depends on twikit version, falling back to standard if needed
                                            try:
                                                recent_tweets = await tw_user.get_tweets('Tweets', count=10)
                                                
                                                relevant_tweets = []
                                                total_engagement = 0
                                                
                                                for tweet in recent_tweets:
                                                    text = tweet.text.lower()
                                                    # Check if tweet mentions the platform or related terms (quest, points, etc)
                                                    if platform_name in text or any(kw in text for kw in ['quest', 'points', 'rank', 'leaderboard', 'referral']):
                                                        engagement = tweet.favorite_count + tweet.retweet_count + (tweet.quote_count or 0)
                                                        total_engagement += engagement
                                                        relevant_tweets.append({
                                                            "text": tweet.text[:100] + "...",
                                                            "date": tweet.created_at,
                                                            "likes": tweet.favorite_count,
                                                            "retweets": tweet.retweet_count,
                                                            "engagement_score": engagement
                                                        })
                                                
                                                user['relevant_tweets'] = relevant_tweets
                                                user['platform_engagement_score'] = total_engagement
                                                
                                                if relevant_tweets:
                                                    print(f"    ! Found {len(relevant_tweets)} relevant tweets with {total_engagement} engagement")
                                            except Exception as tweet_err:
                                                print(f"    ! Could not fetch tweets: {tweet_err}")

                                        print(f"    + Enriched @{handle}")
                                        await asyncio.sleep(1) # Rate limit precaution
                                    except Exception as e:
                                        print(f"    ! Failed to enrich @{handle}: {e}")
                        
                        # Save enriched data
                        with open(f"{safe_name}_data.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2)
                            
                        if current_users:
                            all_users_data.extend(current_users)

                    except json.JSONDecodeError:
                        print(f"  [Raw Text] {page_url}")
                        with open(f"{safe_name}_raw.txt", "w", encoding="utf-8") as f:
                            f.write(result.extracted_content)
                else:
                    print(f"  [No Data] {page_url}")
            else:
                print(f"Error processing {url}: {result.error_message}")
            print("-" * 50)
            
        # Final Analysis Report
        if all_users_data:
            print("\n=== GENERATING ANALYSIS REPORT ===")
            # Convert to DataFrame-like structure for simple analysis
            # (Using pure python to avoid pandas dependency if not installed, but logic is similar)
            
            high_followers_points = []
            low_followers_points = []
            engagement_correlation = [] # (engagement_score, points)
            
            for u in all_users_data:
                points = str(u.get('points_or_score', '0')).replace(',', '').replace(' XP', '').replace(' Points', '')
                try:
                    points = float(points)
                except:
                    points = 0
                    
                followers = u.get('twitter_stats', {}).get('followers', 0)
                platform_engagement = u.get('platform_engagement_score', 0)
                
                if followers > 10000:
                    high_followers_points.append(points)
                elif followers > 0: # Only count if we actually found twitter data
                    low_followers_points.append(points)
                    
                if platform_engagement > 0 and points > 0:
                    engagement_correlation.append((platform_engagement, points))
            
            avg_high = sum(high_followers_points) / len(high_followers_points) if high_followers_points else 0
            avg_low = sum(low_followers_points) / len(low_followers_points) if low_followers_points else 0
            
            print(f"Analysis of {len(all_users_data)} users:")
            print(f"Users with >10k Followers: {len(high_followers_points)}")
            print(f"  Average Points: {avg_high:.2f}")
            print(f"Users with <10k Followers: {len(low_followers_points)}")
            print(f"  Average Points: {avg_low:.2f}")
            
            if engagement_correlation:
                # Simple correlation check
                print(f"\nTweet Engagement Analysis ({len(engagement_correlation)} users):")
                # Sort by engagement
                engagement_correlation.sort(key=lambda x: x[0], reverse=True)
                top_engagers = engagement_correlation[:5]
                
                print("Top 5 Users by Tweet Engagement vs Points:")
                for eng, pts in top_engagers:
                    print(f"  Engagement: {eng} -> Points: {pts}")
                    
                # Check if high engagement correlates with high points
                high_eng_pts = [p for e, p in engagement_correlation if e > 100]
                low_eng_pts = [p for e, p in engagement_correlation if e <= 100]
                
                avg_high_eng = sum(high_eng_pts) / len(high_eng_pts) if high_eng_pts else 0
                avg_low_eng = sum(low_eng_pts) / len(low_eng_pts) if low_eng_pts else 0
                
                if avg_high_eng > avg_low_eng:
                    print(f"  ✅ Insight: High tweet engagement (>100) correlates with higher points ({avg_high_eng:.0f} vs {avg_low_eng:.0f}).")
                    print("     This suggests 'Shilling' or social farming is effective.")
                else:
                    print("  ℹ️  Insight: Tweet engagement does not seem to directly drive points.")
            
            if avg_high > avg_low * 1.5:
                print("\n⚠️  Observation: Larger accounts seem to have significantly higher points.")
            elif avg_high < avg_low:
                print("\n✅ Observation: System appears fair or favors activity over follower count.")
            else:
                print("\nℹ️  Observation: No massive disparity detected based on follower count alone.")
                
            print(f"\nFull extracted dataset saved to individual JSON files.")

if __name__ == "__main__":
    # Fix for Windows asyncio loop policy to support Playwright subprocesses
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
