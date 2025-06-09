import feedparser
import requests
from datetime import datetime

def fetch_google_news():
    url = "https://news.google.com/rss/search?q=alexa+plus+OR+alexa+%2B"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        if "alexa +" in entry.title.lower() or "alexa plus" in entry.title.lower():
            articles.append((entry.title, entry.link))
    return articles

def fetch_reddit():
    url = "https://www.reddit.com/search.json?q=%22alexa+plus%22+OR+%22alexa+%2B%22&sort=new"
    headers = {'User-agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    posts = []
    if resp.status_code == 200:
        data = resp.json()
        for child in data['data']['children']:
            post = child['data']
            title = post.get('title', '')
            permalink = post.get('permalink', '')
            if "alexa +" in title.lower() or "alexa plus" in title.lower():
                posts.append((title, f"https://reddit.com{permalink}"))
    return posts

def fetch_blog_rss(feed_url):
    feed = feedparser.parse(feed_url)
    posts = []
    for entry in feed.entries:
        if "alexa +" in entry.title.lower() or "alexa plus" in entry.title.lower():
            posts.append((entry.title, entry.link))
    return posts

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"alexa-plus-summary-{today}.md"
    summary = []

    # Google News
    news = fetch_google_news()
    if news:
        summary.append("### News Articles")
        for title, link in news:
            summary.append(f"- [{title}]({link})")
    else:
        summary.append("### News Articles\n- No recent news found.")

    # Reddit
    reddit = fetch_reddit()
    if reddit:
        summary.append("\n### Reddit Posts")
        for title, link in reddit:
            summary.append(f"- [{title}]({link})")
    else:
        summary.append("\n### Reddit Posts\n- No recent Reddit posts found.")

    # Blogs (add more feeds as needed)
    blogs = []
    tech_blogs = [
        "https://www.theverge.com/rss/index.xml",
        "https://techcrunch.com/feed/",
    ]
    for feed_url in tech_blogs:
        blogs += fetch_blog_rss(feed_url)
    if blogs:
        summary.append("\n### Blog Posts")
        for title, link in blogs:
            summary.append(f"- [{title}]({link})")
    else:
        summary.append("\n### Blog Posts\n- No recent blog posts found.")

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Alexa Plus Daily Summary ({today})\n\n")
        f.write("\n".join(summary))

if __name__ == "__main__":
    main()
