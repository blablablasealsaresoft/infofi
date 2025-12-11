print("Start check")
try:
    from crawl4ai import CrawlerRunConfig
    from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
    print("Deep crawling modules found.")
except ImportError as e:
    print(f"Deep crawling modules NOT found: {e}")
print("End check")
