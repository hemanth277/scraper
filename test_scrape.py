import requests
from bs4 import BeautifulSoup

def scrape_results(query):
    url = "https://duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://duckduckgo.com/",
        "Connection": "keep-alive"
    }
    params = {"q": query}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Status: {response.status_code}")
        print(f"Response length: {len(response.text)}")
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.select("a.result__a"):
            title = result.get_text(strip=True)
            link = result.get("href")
            if title and link:
                results.append({"Title": title, "Link": link})
        return results
    except Exception as e:
        print("Error:", e)
        return []

if __name__ == "__main__":
    with open("test_output.txt", "w", encoding="utf-8") as f:
        f.write("Starting scrape test...\n")
        results = scrape_results("python")
        f.write(f"Scraped {len(results)} results.\n")
        for r in results[:3]:
            f.write(str(r) + "\n")
    print("Done. Check test_output.txt")
