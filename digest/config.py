"""Paths, environment, and the editable feed list."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "posts"
DOCS_DIR = ROOT / "docs"
DATA_DIR = ROOT / "data"
FEEDS_FILE = ROOT / "feeds.yaml"
PACKAGE_DIR = Path(__file__).resolve().parent

# gemini-2.0-flash is retired (404). Override with GEMINI_MODEL if needed.
DEFAULT_MODEL = "gemini-3.6-flash"

load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class Feed:
    id: str
    name: str
    url: str
    homepage: str = ""


@dataclass(frozen=True)
class SiteConfig:
    title: str
    tagline: str
    max_items: int
    model: str


def utc_today() -> date:
    return datetime.now(timezone.utc).date()


def parse_date(value: str | None) -> date:
    if not value:
        return utc_today()
    return date.fromisoformat(value)


def load_raw() -> dict:
    return yaml.safe_load(FEEDS_FILE.read_text(encoding="utf-8")) or {}


def load_feeds() -> list[Feed]:
    rows = load_raw().get("feeds") or []
    return [
        Feed(
            id=row["id"],
            name=row["name"],
            url=row["url"],
            homepage=row.get("homepage", ""),
        )
        for row in rows
    ]


def load_site() -> SiteConfig:
    raw = load_raw()
    site = raw.get("site") or {}
    return SiteConfig(
        title=site.get("title", "Daily Digest"),
        tagline=site.get("tagline", "RSS, summarized each day."),
        max_items=int(raw.get("max_items", 12)),
        model=os.environ.get("GEMINI_MODEL") or str(raw.get("model", DEFAULT_MODEL)),
    )


def gemini_api_key() -> str:
    return os.environ.get("GEMINI_API_KEY", "").strip()
