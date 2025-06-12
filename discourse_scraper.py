import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = f"{BASE_URL}/c/courses/tds-kb/34"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_topic_links():
    print("🔍 Fetching topic links...")
    res = requests.get(CATEGORY_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "/t/" in href and not href.startswith("http"):
            full_url = urljoin(BASE_URL, href)
            links.add(full_url.split('?')[0])
    return list(links)

def get_post_content(topic_url):
    res = requests.get(topic_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    post_texts = soup.find_all("div", class_="cooked")
    text = "\n\n".join(p.get_text(separator=" ", strip=True) for p in post_texts)
    return text

def scrape_discourse(limit=50):
    links = get_topic_links()
    print(f"✅ Found {len(links)} topics.")
    results = []
    for i, link in enumerate(links[:limit]):
        try:
            print(f"[{i+1}/{limit}] Scraping: {link}")
            text = get_post_content(link)
            results.append({"url": link, "text": text})
            time.sleep(1)  # Be kind to server
        except Exception as e:
            print(f"❌ Error scraping {link}: {e}")
    return results

if __name__ == "__main__":
    scraped = scrape_discourse(limit=50)
    with open("discourse_data.json", "w", encoding="utf-8") as f:
        json.dump(scraped, f, indent=2, ensure_ascii=False)
    print("✅ Done! Saved to discourse_data.json")
