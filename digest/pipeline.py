"""Orchestrate fetch → summarize → build. CLI commands stay thin here."""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

import httpx

from digest.config import DATA_DIR, Feed, load_feeds, load_site
from digest.feeds import FeedItem, fetch_all, items_as_dicts
from digest.gemini import digest_prompt, generate, require_api_key, split_title
from digest.images import try_write_header
from digest.posts import Post, write_post
from digest.site import build as build_site

log = logging.getLogger(__name__)


def fetch(day: date) -> dict[str, list[FeedItem]]:
    site = load_site()
    feeds = load_feeds()
    log.info("Fetching %s feed(s) for %s", len(feeds), day.isoformat())
    by_id = fetch_all(feeds, day, site.max_items)
    _save_fetch(day, by_id)
    return by_id


def summarize(day: date) -> list[Path]:
    require_api_key()
    site = load_site()
    log.info("Summarizing with Gemini model %s", site.model)
    log.info("Header images with Gemini image model %s", site.image_model)
    feeds = {feed.id: feed for feed in load_feeds()}
    by_id = _load_fetch(day)
    if not by_id:
        log.warning("No fetched items for %s. Run fetch first.", day.isoformat())
        return []

    written: list[Path] = []
    for feed_id, items in by_id.items():
        feed = feeds.get(feed_id)
        if feed is None:
            log.warning("Skipping unknown feed id %s", feed_id)
            continue
        if not items:
            log.info("No items for %s on %s — skipping", feed_id, day.isoformat())
            continue
        path = _summarize_feed(feed, day, items, site.model, site.image_model)
        if path:
            written.append(path)
    return written


def build() -> Path:
    docs = build_site()
    log.info("Wrote site to %s", docs)
    return docs


def run(day: date) -> None:
    fetch(day)
    summarize(day)
    build()


def _summarize_feed(
    feed: Feed, day: date, items: list[dict], model: str, image_model: str
) -> Path | None:
    prompt = digest_prompt(feed.name, day.isoformat(), items)
    try:
        markdown = generate(prompt, model)
    except (httpx.HTTPError, RuntimeError) as exc:
        log.warning("Gemini failed for %s: %s", feed.id, exc)
        return None
    title, body = split_title(markdown)
    post = Post(
        slug=feed.id,
        title=title or f"{feed.name} — {day.isoformat()}",
        date=day.isoformat(),
        source=feed.name,
        source_url=feed.homepage or feed.url,
        body=body,
    )
    path = write_post(post)
    log.info("Wrote %s", path)
    rel = try_write_header(post, model=image_model)
    if rel:
        post.header_image = rel
        path = write_post(post)
    return path


def _save_fetch(day: date, by_id: dict[str, list[FeedItem]]) -> None:
    folder = DATA_DIR / day.isoformat()
    folder.mkdir(parents=True, exist_ok=True)
    for feed_id, items in by_id.items():
        path = folder / f"{feed_id}.json"
        path.write_text(json.dumps(items_as_dicts(items), indent=2) + "\n", encoding="utf-8")


def _load_fetch(day: date) -> dict[str, list[dict]]:
    folder = DATA_DIR / day.isoformat()
    if not folder.is_dir():
        return {}
    out: dict[str, list[dict]] = {}
    for path in sorted(folder.glob("*.json")):
        out[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return out
