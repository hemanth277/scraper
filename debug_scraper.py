import requests
from bs4 import BeautifulSoup

def scrape_url_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            print(f"Found {len(paragraphs)} paragraphs.")
            text_content = " ".join([p.get_text().strip() for p in paragraphs[:8]])
            return text_content if len(text_content) > 50 else "No significant text content found."
    except Exception as e:
        return f"Error: {e}"
    return "Failed"

if __name__ == "__main__":
    urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://www.space.com/news"
    ]
    for url in urls:
        print("-" * 20)
        content = scrape_url_content(url)
        print(f"Result (first 100 chars): {content[:100]}...")
