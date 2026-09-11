"""Markdown posts with YAML front matter — one file per source per day."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from digest.config import POSTS_DIR

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n?(.*)\Z", re.S)


@dataclass
class Post:
    slug: str
    title: str
    date: str
    source: str
    source_url: str
    body: str
    header_image: str = ""
    path: Path | None = None

    def excerpt(self, limit: int = 220) -> str:
        text = re.sub(r"[#*_>`\[\]]", "", self.body)
        text = " ".join(text.split())
        if len(text) <= limit:
            return text
        return text[:limit].rsplit(" ", 1)[0] + "…"


def post_path(day: date | str, slug: str) -> Path:
    return POSTS_DIR / str(day) / f"{slug}.md"


def write_post(post: Post) -> Path:
    path = post_path(post.date, post.slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        "title": post.title,
        "date": post.date,
        "source": post.source,
        "source_url": post.source_url,
        "slug": post.slug,
    }
    if post.header_image:
        meta["header_image"] = post.header_image
    body = (
        "---\n"
        f"{yaml.safe_dump(meta, sort_keys=False).strip()}\n"
        "---\n\n"
        f"{post.body.strip()}\n"
    )
    path.write_text(body, encoding="utf-8")
    post.path = path
    return path


def parse_post(path: Path) -> Post:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    meta = yaml.safe_load(match.group(1)) or {}
    raw_date = meta.get("date", path.parent.name)
    date_str = raw_date.isoformat() if hasattr(raw_date, "isoformat") else str(raw_date)
    return Post(
        slug=str(meta.get("slug") or path.stem),
        title=str(meta.get("title") or path.stem),
        date=date_str,
        source=str(meta.get("source") or ""),
        source_url=str(meta.get("source_url") or ""),
        body=match.group(2).strip(),
        header_image=str(meta.get("header_image") or ""),
        path=path,
    )


def load_all_posts() -> list[Post]:
    posts = [parse_post(path) for path in sorted(POSTS_DIR.glob("*/*.md"))]
    posts.sort(key=lambda post: (post.date, post.slug), reverse=True)
    return posts


def group_by_date(posts: list[Post]) -> dict[str, list[Post]]:
    grouped: dict[str, list[Post]] = {}
    for post in posts:
        grouped.setdefault(post.date, []).append(post)
    return dict(sorted(grouped.items(), reverse=True))
