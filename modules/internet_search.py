"""RSS-based sustainability intelligence search with graceful offline handling."""

from __future__ import annotations

import re
from html import unescape

try:
    import feedparser
except ImportError:  # pragma: no cover - supports app startup before dependencies are installed.
    feedparser = None

try:
    import requests
except ImportError:  # pragma: no cover - supports app startup before dependencies are installed.
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - supports app startup before dependencies are installed.
    BeautifulSoup = None

from modules.news_summarizer import simple_summary
from modules.relevance_classifier import classify_relevance_to_tpc, classify_topic, suggest_action


def clean_text(text: str) -> str:
    """Remove HTML tags and extra spacing from feed text."""

    if not text:
        return ""
    if BeautifulSoup is None:
        cleaned = re.sub(r"<[^>]+>", " ", unescape(text))
    else:
        soup = BeautifulSoup(unescape(text), "html.parser")
        cleaned = soup.get_text(" ")
    return re.sub(r"\s+", " ", cleaned).strip()


def get_default_feeds() -> list[dict[str, str]]:
    """Return public RSS feeds and pages used for sustainability intelligence."""

    return [
        {"source": "IFRS Foundation", "url": "https://www.ifrs.org/news-and-events/news/rss/"},
        {"source": "GRI", "url": "https://www.globalreporting.org/news/news-center/rss/"},
        {"source": "IMO", "url": "https://www.imo.org/en/MediaCentre/PressBriefings/Pages/RSS.aspx"},
        {"source": "European Commission", "url": "https://ec.europa.eu/commission/presscorner/api/rss?language=en"},
        {"source": "UN Global Compact", "url": "https://unglobalcompact.org/news.atom"},
        {"source": "Carbon Brief", "url": "https://www.carbonbrief.org/feed/"},
        {"source": "ESG Today", "url": "https://www.esgtoday.com/feed/"},
        {"source": "MarineLink", "url": "https://www.marinelink.com/news/rss"},
        {"source": "Seatrade Maritime News", "url": "https://www.seatrade-maritime.com/rss.xml"},
    ]


def fetch_rss_feed(feed_url: str) -> list[dict[str, str]]:
    """Fetch one RSS feed and return normalized entries.

    Any network or parsing problem returns an empty list so the app can keep
    running when internet access is blocked.
    """

    if requests is None or feedparser is None:
        return []

    try:
        response = requests.get(feed_url, timeout=10, headers={"User-Agent": "TPC Sustainability Reporting Copilot"})
        response.raise_for_status()
    except requests.RequestException:
        return []

    parsed = feedparser.parse(response.content)
    entries = []
    for entry in parsed.entries:
        summary_source = entry.get("summary", "") or entry.get("description", "")
        text = clean_text(f"{entry.get('title', '')}. {summary_source}")
        entries.append(
            {
                "Title": clean_text(entry.get("title", "Untitled")),
                "Source": "",
                "Date": entry.get("published", "") or entry.get("updated", ""),
                "Link": entry.get("link", ""),
                "Raw Text": text,
                "Short Summary": simple_summary(text),
            }
        )
    return entries


def filter_results(results: list[dict[str, str]], query: str) -> list[dict[str, str]]:
    """Filter RSS results by query terms and sustainability keywords."""

    query_terms = [term.lower() for term in re.findall(r"[A-Za-z0-9]+", query or "") if len(term) > 2]
    sustainability_terms = [
        "issb",
        "gri",
        "climate",
        "carbon",
        "emissions",
        "maritime",
        "shipping",
        "assurance",
        "fuel",
        "sustainability",
        "net",
        "transition",
        "imo",
        "ets",
    ]
    filtered = []
    for item in results:
        haystack = f"{item.get('Title', '')} {item.get('Raw Text', '')}".lower()
        query_match = not query_terms or any(term in haystack for term in query_terms)
        sustainability_match = any(term in haystack for term in sustainability_terms)
        if query_match and sustainability_match:
            filtered.append(item)
    return filtered


def search_feeds(query: str, max_results: int = 20) -> list[dict[str, str]]:
    """Search default RSS feeds and enrich results for the Streamlit page."""

    all_results = []
    for feed in get_default_feeds():
        entries = fetch_rss_feed(feed["url"])
        for entry in entries:
            entry["Source"] = feed["source"]
            text = f"{entry.get('Title', '')} {entry.get('Raw Text', '')}"
            entry["Topic Classification"] = classify_topic(text)
            entry["Relevance to TPC Group"] = classify_relevance_to_tpc(text)
            entry["Suggested Action"] = suggest_action(text)
            all_results.append(entry)

    filtered = filter_results(all_results, query)
    return filtered[:max_results]
