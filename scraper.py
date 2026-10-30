import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_generic_news(source_name, url, limit=4):
    """प्राय: सबै न्युज पोर्टलका लागि काम गर्ने जेनेरिक स्क्र्यापर"""
    articles = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # प्राय नेपाली न्युज साइटहरूले h1, h2, h3 भित्र हेडलाइन राख्छन्
        headlines = soup.find_all(['h1', 'h2', 'h3'])
        
        seen = set()
        for item in headlines:
            a = item.find('a')
            if a and a.text.strip():
                title = a.text.strip().replace('\n', ' ').strip()
                link = a.get('href', '')
                
                # यदि लिंक रिलेटिभ (/story/123) छ भने डोमेन जोड्ने
                if link and not link.startswith('http'):
                    base_url = url.rstrip('/')
                    if not link.startswith('/'):
                        link = '/' + link
                    link = base_url + link
                    
                # हेडलाइन धेरै सानो नहोस् र दोहोरिन नपाओस्
                if link and title not in seen and len(title) > 20:
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

    # तपाईँले थप्न चाहनुभएका सबै न्युज पोर्टलहरू:
    sources = [
        {"name": "अनलाइनखबर", "url": "https://www.onlinekhabar.com/"},
        {"name": "कान्तिपुर", "url": "https://ekantipur.com/"},
        {"name": "सेतोपाटी", "url": "https://www.setopati.com/"},
        {"name": "रातोपाटी", "url": "https://www.ratopati.com/"},
        {"name": "नागरिक न्युज", "url": "https://nagariknews.nagariknetwork.com/"},
        {"name": "उज्यालो अनलाइन", "url": "https://ujyaaloonline.com/"},
        {"name": "इमेजखबर", "url": "https://www.imagekhabar.com/"},
        {"name": "बिजमाण्डू", "url": "https://bizmandu.com/"}
    ]

    print("सबै न्युज पोर्टलहरूबाट ताजा समाचार संकलन गरिँदैछ...")
    for src in sources:
        print(f"तान्दै: {src['name']}")
        news_items = fetch_generic_news(src['name'], src['url'], limit=4)
        all_news.extend(news_items)

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"जम्मा {len(all_news)} वटा समाचार सफलतापुर्वक news.json मा सेभ भयो।")

if __name__ == "__main__":
    main()
