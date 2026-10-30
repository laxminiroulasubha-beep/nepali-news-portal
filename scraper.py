import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_news(source_name, url, limit=5):
    articles = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        headlines = soup.find_all(['h2', 'h3'])
        
        seen = set()
        for item in headlines:
            a = item.find('a')
            if a and a.text.strip():
                title = a.text.strip()
                link = a.get('href', '')
                if not link.startswith('http'):
                    link = url.rstrip('/') + link
                if title not in seen and len(title) > 20:
                    seen.add(title)
                    articles.append({
                        "title": title,
                        "link": link,
                        "source": source_name
                    })
                    if len(articles) >= limit:
                        break
    except Exception as e:
        print(f"Error fetching from {source_name}: {e}")
    return articles

def main():
    all_news = []
    all_news.extend(fetch_news("अनलाइनखबर", "https://www.onlinekhabar.com/"))
    all_news.extend(fetch_news("रातोपाटी", "https://www.ratopati.com/"))
    all_news.extend(fetch_news("सेतोपाटी", "https://www.setopati.com/"))

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    print("समाचार सफलतापुर्वक news.json मा सेभ भयो।")

if __name__ == "__main__":
    main()
