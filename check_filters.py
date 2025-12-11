import sys
import os

# Redirect stdout to a file
sys.stdout = open('output_check.txt', 'w')
sys.stderr = sys.stdout

try:
    import crawl4ai
    print(f"crawl4ai version: {crawl4ai.__version__}")
except:
    print("crawl4ai version not found")

try:
    import crawl4ai.deep_crawling
    print(f"deep_crawling dir: {dir(crawl4ai.deep_crawling)}")
    
    try:
        from crawl4ai.deep_crawling import filters
        print(f"filters imported: {filters}")
        print(f"filters dir: {dir(filters)}")
    except ImportError as e:
        print(f"Could not import filters from deep_crawling: {e}")
        
    # Check if FilterChain is in deep_crawling
    if hasattr(crawl4ai.deep_crawling, 'FilterChain'):
        print("FilterChain is in crawl4ai.deep_crawling")
        
except ImportError as e:
    print(f"Could not import deep_crawling: {e}")

try:
    import crawl4ai.filters
    print("Found crawl4ai.filters")
except ImportError:
    print("crawl4ai.filters not found")
