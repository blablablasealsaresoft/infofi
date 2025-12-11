import crawl4ai
import inspect
import pkgutil

print(f"crawl4ai file: {crawl4ai.__file__}")

# Try to find deep_crawling
try:
    from crawl4ai import deep_crawling
    print(f"deep_crawling found: {deep_crawling}")
    print(f"dir(deep_crawling): {dir(deep_crawling)}")
except ImportError as e:
    print(f"Error importing deep_crawling: {e}")

# Try to find where FilterChain is
try:
    import crawl4ai
    # search for FilterChain in all submodules
    found = False
    for loader, module_name, is_pkg in pkgutil.walk_packages(crawl4ai.__path__, crawl4ai.__name__ + "."):
        try:
            module = __import__(module_name, fromlist="dummy")
            if hasattr(module, "FilterChain"):
                print(f"Found FilterChain in {module_name}")
                found = True
        except Exception:
            pass
    if not found:
        print("FilterChain not found in walk_packages")

except Exception as e:
    print(f"Error during search: {e}")
