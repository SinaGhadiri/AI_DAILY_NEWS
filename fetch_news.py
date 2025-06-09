import feedparser
from datetime import datetime

feed_url = "https://news.google.com/rss/search?q=artificial+intelligence"
feed = feedparser.parse(feed_url)

today = datetime.now().strftime("%Y-%m-%d")
filename = f"_posts/{today}-ai-news.md"

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ntitle: 'AI News for {today}'\n---\n\n")
    for entry in feed.entries[:10]:
        f.write(f"- [{entry.title}]({entry.link})\n")
