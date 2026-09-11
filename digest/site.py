"""Turn posts/ markdown into a static site in docs/ (GitHub Pages)."""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from markupsafe import Markup

from digest.config import DOCS_DIR, PACKAGE_DIR, load_site
from digest.posts import group_by_date, load_all_posts

DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TEMPLATES = PACKAGE_DIR / "templates"
STATIC = PACKAGE_DIR / "static"


def build() -> Path:
    site = load_site()
    posts = load_all_posts()
    by_date = group_by_date(posts)
    dates = list(by_date.keys())
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["longdate"] = _longdate
    env.filters["md"] = _render_markdown

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    _clear_date_dirs(DOCS_DIR)
    _copy_assets()

    _write(
        DOCS_DIR / "index.html",
        env.get_template("home.html"),
        site=site,
        by_date=by_date,
        dates=dates,
        recent=list(by_date.items())[:14],
        root="./",
        active_date=dates[0] if dates else "",
    )
    _write(
        DOCS_DIR / "dates" / "index.html",
        env.get_template("dates.html"),
        site=site,
        dates=dates,
        by_date=by_date,
        root="../",
        active_date="",
    )
    _write(
        DOCS_DIR / "404.html",
        env.get_template("not_found.html"),
        site=site,
        dates=dates,
        root="./",
        active_date="",
    )

    for day, day_posts in by_date.items():
        day_dir = DOCS_DIR / day
        _write(
            day_dir / "index.html",
            env.get_template("day.html"),
            site=site,
            day=day,
            posts=day_posts,
            dates=dates,
            root="../",
            active_date=day,
            prev_date=_neighbor(dates, day, 1),
            next_date=_neighbor(dates, day, -1),
        )
        for post in day_posts:
            _write(
                day_dir / f"{post.slug}.html",
                env.get_template("post.html"),
                site=site,
                post=post,
                day=day,
                dates=dates,
                root="../",
                active_date=day,
            )

    (DOCS_DIR / "dates.json").write_text(json.dumps(dates, indent=2) + "\n", encoding="utf-8")
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")
    return DOCS_DIR


def _write(path: Path, template, **ctx) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template.render(**ctx), encoding="utf-8")


def _copy_assets() -> None:
    dest = DOCS_DIR / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for file in STATIC.iterdir():
        if file.is_file():
            shutil.copy2(file, dest / file.name)
    # Header PNGs live in docs/assets/headers/ and are left in place.


def _clear_date_dirs(docs: Path) -> None:
    for child in docs.iterdir():
        if child.is_dir() and DATE_DIR.match(child.name):
            shutil.rmtree(child)


def _neighbor(dates: list[str], day: str, offset: int) -> str | None:
    try:
        index = dates.index(day) + offset
    except ValueError:
        return None
    if 0 <= index < len(dates):
        return dates[index]
    return None


def _longdate(value: str) -> str:
    return datetime.strptime(value, "%Y-%m-%d").strftime("%A, %d %B %Y")


def _render_markdown(body: str) -> Markup:
    return Markup(markdown.markdown(body, extensions=["extra", "sane_lists"]))
