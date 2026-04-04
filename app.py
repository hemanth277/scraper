import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify, send_file
import pandas as pd
from ddgs import DDGS
import traceback
import os

app = Flask(__name__)

# global storage for session-like persistence
stored_results = []

def get_smart_summary(query):
    """
    Attempts to get a clean, high-accuracy direct answer for the 'Quick Answer' box.
    """
    try:
        api_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        api_response = requests.get(api_url, timeout=4)
        if api_response.status_code == 200:
            data = api_response.json()
            if data.get("AbstractText"):
                return data.get("AbstractText")
    except:
        pass
    return None

def scrape_url_content(url):
    """
    Fetches the HTML of a URL and extracts the main text content.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract text from paragraphs, but limit to avoid massive data
            paragraphs = soup.find_all("p")
            text_content = " ".join([p.get_text().strip() for p in paragraphs[:8]]) # top 8 paragraphs
            return text_content if len(text_content) > 50 else "No significant text content found."
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None

def scrape_results(query):
    """
    Fetches results and returns only those with successfully extracted deep content.
    """
    results = []
    try:
        print(f"[*] Scraping structured data for: {query}")
        with DDGS() as ddgs:
            # Fetch slightly more to ensure we get enough successful scrapes
            ddgs_results = list(ddgs.text(query, max_results=12))
            
            for i, r in enumerate(ddgs_results):
                link = r.get("href", "#")
                if link == "#":
                    continue
                
                # Scrape only one result as requested
                if len(results) < 1:
                    print(f"[*] Extracting deep data from: {link}")
                    content = scrape_url_content(link)
                    
                    if content and content != "No significant text content found.":
                        results.append({
                            "Title": r.get("title", "No Title"),
                            "Link": link,
                            "ExtractedContent": content
                        })
                else:
                    break
                
        print(f"[+] Scraped {len(results)} successful results")
        return results
    except Exception as e:
        print(f"[!] Scraping Error: {e}")
        return results

@app.route("/", methods=["GET", "POST"])
def index():
    global stored_results

    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            return render_template("index.html", error="Please enter a search term")

        # Get the smart summary (if available)
        summary = get_smart_summary(query)
        
        # Get full results
        stored_results = scrape_results(query)

        return render_template(
            "results.html",
            results=stored_results,
            query=query,
            summary=summary
        )

    return render_template("index.html")

@app.route("/download")
def download():
    if not stored_results:
        return "No data to download", 400

    try:
        df = pd.DataFrame(stored_results)
        file_path = "results.xlsx"
        df.to_excel(file_path, index=False)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)