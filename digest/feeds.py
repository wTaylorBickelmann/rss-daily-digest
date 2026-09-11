"""Fetch and filter RSS/Atom items. A broken feed is skipped, not fatal."""

from __future__ import annotations

import logging
import re
import socket
from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timezone
from time import struct_time

import feedparser

from digest.config import Feed

log = logging.getLogger(__name__)

USER_AGENT = "rss-daily-digest/0.1"
socket.setdefaulttimeout(30)


@dataclass
class FeedItem:
    title: str
    link: str
    summary: str
    published: str


def _as_utc(parsed: struct_time | None) -> datetime | None:
    if not parsed:
        return None
    return datetime(*parsed[:6], tzinfo=timezone.utc)


def _plain(html: str, limit: int = 400) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    return " ".join(text.split())[:limit]


def fetch_feed(feed: Feed, day: date, max_items: int) -> list[FeedItem]:
    parsed = feedparser.parse(feed.url, agent=USER_AGENT)
    if parsed.bozo and not parsed.entries:
        raise RuntimeError(parsed.bozo_exception or "unreadable feed")

    start = datetime.combine(day, time.min, tzinfo=timezone.utc)
    dated: list[FeedItem] = []
    undated: list[FeedItem] = []

    for entry in parsed.entries:
        item = FeedItem(
            title=(entry.get("title") or "(untitled)").strip(),
            link=(entry.get("link") or "").strip(),
            summary=_plain(entry.get("summary") or entry.get("description") or ""),
            published="",
        )
        published_dt = _as_utc(entry.get("published_parsed") or entry.get("updated_parsed"))
        if published_dt is None:
            undated.append(item)
            continue
        item.published = published_dt.date().isoformat()
        if published_dt >= start:
            dated.append(item)

    chosen = dated or undated[:max_items]
    return chosen[:max_items]


def fetch_all(feeds: list[Feed], day: date, max_items: int) -> dict[str, list[FeedItem]]:
    out: dict[str, list[FeedItem]] = {}
    for feed in feeds:
        try:
            items = fetch_feed(feed, day, max_items)
        except Exception as exc:
            log.warning("Skipping feed %s (%s): %s", feed.id, feed.url, exc)
            continue
        log.info("%s: %s item(s)", feed.id, len(items))
        out[feed.id] = items
    return out


def items_as_dicts(items: list[FeedItem]) -> list[dict]:
    return [asdict(item) for item in items]
