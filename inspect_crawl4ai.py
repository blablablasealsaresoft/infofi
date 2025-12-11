import crawl4ai
import os
import pkgutil
import sys

output_file = os.path.join(os.getcwd(), "crawl4ai_structure.txt")

with open(output_file, "w") as f:
    f.write(f"crawl4ai file: {crawl4ai.__file__}\n")
    f.write(f"crawl4ai path: {crawl4ai.__path__}\n")
    
    # List all submodules
    f.write("\nSubmodules:\n")
    for loader, module_name, is_pkg in pkgutil.walk_packages(crawl4ai.__path__, crawl4ai.__name__ + "."):
        f.write(f"{module_name}\n")
        
    # Check for FilterChain specifically
    f.write("\nChecking for FilterChain:\n")
    try:
        from crawl4ai.deep_crawling import filters
        f.write(f"Successfully imported crawl4ai.deep_crawling.filters\n")
        if hasattr(filters, 'FilterChain'):
            f.write("FilterChain found in crawl4ai.deep_crawling.filters\n")
        else:
            f.write("FilterChain NOT found in crawl4ai.deep_crawling.filters\n")
    except ImportError as e:
        f.write(f"Failed to import crawl4ai.deep_crawling.filters: {e}\n")
        
    # Check deep_crawling content
    try:
        from crawl4ai import deep_crawling
        f.write(f"\ncrawl4ai.deep_crawling content: {dir(deep_crawling)}\n")
    except ImportError as e:
        f.write(f"Failed to import crawl4ai.deep_crawling: {e}\n")

print(f"Structure written to {output_file}")
