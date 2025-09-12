import feedparser
import psycopg2
import os
import json

DATABASE_URL = os.environ["SUPABASE_DB_URL"]

with open("rss_feeds.json", "r", encoding="utf-8") as f:
    rss_feeds = json.load(f)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

for category, urls in rss_feeds.items():
    for rss_url in urls:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            link = entry.link
            try:
                cur.execute(
                    """
                    INSERT INTO news_links (category, url)
                    VALUES (%s, %s)
                    ON CONFLICT (url) DO NOTHING;
                    """,
                    (category, link)
                )
            except Exception as e:
                print(f"[ERROR] {e} - {link}")

conn.commit()
cur.close()
conn.close()
