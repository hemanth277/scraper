import duckduckgo_search
from duckduckgo_search import DDGS

print(f"Version: {duckduckgo_search.__version__}")

def test():
    print("Starting test...")
    try:
        with DDGS() as ddgs:
            # Try a different method or more results
            results = list(ddgs.text("python", max_results=5))
            print(f"Results Count: {len(results)}")
            for r in results:
                print(r)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
