import requests

def test_instant_answer(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        response = requests.get(url)
        data = response.json()
        print(f"Query: {query}")
        print(f"Abstract: {data.get('AbstractText')}")
        print(f"Answer: {data.get('Answer')}")
        print(f"Definition: {data.get('Definition')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_instant_answer("capital of France")
    print("-" * 20)
    test_instant_answer("python programming language")
