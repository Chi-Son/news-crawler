import feedparser
import json
import os
from supabase import create_client, Client

# ---- Lấy env ----
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]

# Tạo client supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ---- Load RSS feeds từ file JSON ----
with open("feeds.json", "r", encoding="utf-8") as f:
    rss_feeds = json.load(f)

# ---- Crawl RSS và insert ----
for category, urls in rss_feeds.items():
    for rss_url in urls:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            link = entry.link
            try:
                # Insert vào Supabase, ignore duplicate
                supabase.table("news_links").upsert(
                    {"category": category, "url": link},
                    on_conflict="url"
                ).execute()
            except Exception as e:
                print(f"[ERROR] {e} - {link}")

print("✅ Done crawling and inserting RSS links.")

