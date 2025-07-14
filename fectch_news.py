import os
import requests
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# 1.  Load your NewsAPI key
# ─────────────────────────────────────────────
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# ─────────────────────────────────────────────
# 2.  Domain categories
# ─────────────────────────────────────────────
tech_domains = {
    "theverge.com",
    "technologyreview.com",
    "wired.com",
    "techcrunch.com",
    "techradar.com",
    "thenextweb.com",
}

business_domains = {
    "wsj.com",
    "businessinsider.com",
    "ft.com",
    "cnbc.com",
    "bloomberg.com",
    "time.com",
}

general_domains = {
    "reuters.com",
    "theguardian.com",
    "nytimes.com",
    "bbc.com",
    "cnn.com",
    "nbcnews.com",
    "washingtonpost.com",
}

# Explicit mapping from NewsAPI source names → domains
name_to_domain = {
    "The Verge": "theverge.com",
    "Wired": "wired.com",
    "MIT Technology Review": "technologyreview.com",
    "TechCrunch": "techcrunch.com",
    "TechRadar": "techradar.com",
    "The Next Web": "thenextweb.com",
    "The Wall Street Journal": "wsj.com",
    "Business Insider": "businessinsider.com",
    "Financial Times": "ft.com",
    "CNBC": "cnbc.com",
    "Bloomberg": "bloomberg.com",
    "TIME": "time.com",
    "Reuters": "reuters.com",
    "The Guardian": "theguardian.com",
    "The New York Times": "nytimes.com",
    "BBC News": "bbc.com",
    "CNN": "cnn.com",
    "NBC News": "nbcnews.com",
    "The Washington Post": "washingtonpost.com",
}

# Combined domain list for the NewsAPI request
ai_domains = list(tech_domains | business_domains | general_domains)
domain_str = ",".join(ai_domains)

# ─────────────────────────────────────────────
# 3.  Build and send the NewsAPI request
# ─────────────────────────────────────────────
url = (
    "https://newsapi.org/v2/everything?"
    "q=artificial+intelligence+OR+AI&"
    "from=2025-07-12&"
    "to=2025-07-14&"
    "sortBy=popularity&"
    f"domains={domain_str}&"
    f"apiKey={NEWSAPI_KEY}"
)

response = requests.get(url)
data = response.json()

# ─────────────────────────────────────────────
# 4.  Categorize the articles
# ─────────────────────────────────────────────
business_articles, tech_articles, general_articles = [], [], []

for art in data.get("articles", []):
    source_name = art["source"]["name"]
    domain = name_to_domain.get(source_name, "").lower()

    article = {
        "source": source_name,
        "title": art["title"],
        "description": art.get("description", "No description available."),
        "url": art["url"],
        "published_at": art["publishedAt"][:10],  # YYYY-MM-DD
    }

    if domain in tech_domains:
        tech_articles.append(article)
    elif domain in business_domains:
        business_articles.append(article)
    elif domain in general_domains:
        general_articles.append(article)

# ─────────────────────────────────────────────
# 5.  Pretty-print the results
# ─────────────────────────────────────────────
def print_articles(label, articles):
    print(f"\n📚 {label} ({len(articles)} articles)\n" + "─" * 60)
    for a in articles:
        print(f"📰 {a['source']}  ({a['published_at']})")
        print(f"📌 {a['title']}")
        print(f"🧾 {a['description']}")
        print(f"🔗 {a['url']}\n")

print_articles("Business-Focused AI Articles", business_articles)
print_articles("Tech-Focused AI Articles", tech_articles)
print_articles("General News AI Articles", general_articles)