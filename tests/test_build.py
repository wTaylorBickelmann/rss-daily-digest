import json
import os
import unittest
from datetime import date
from unittest.mock import patch

from digest.config import ROOT, DEFAULT_MODEL, Feed, load_feeds, load_site
from digest.feeds import fetch_all
from digest.gemini import require_api_key
from digest.posts import load_all_posts, parse_post
from digest.site import build


class ConfigTests(unittest.TestCase):
    def test_starter_feeds_have_ids_and_urls(self):
        feeds = load_feeds()
        self.assertGreaterEqual(len(feeds), 5)
        ids = [feed.id for feed in feeds]
        self.assertEqual(len(ids), len(set(ids)))
        for feed in feeds:
            self.assertTrue(feed.url.startswith("http"))

    def test_site_title(self):
        self.assertTrue(load_site().title)

    def test_data_science_feeds_and_model(self):
        ids = {feed.id for feed in load_feeds()}
        self.assertEqual(
            ids,
            {
                "arxiv-cs-lg",
                "towards-data-science",
                "kdnuggets",
                "huggingface-blog",
                "lil-log",
                "sebastian-raschka",
            },
        )
        env = {k: v for k, v in os.environ.items() if k not in {"GEMINI_MODEL", "GEMINI_IMAGE_MODEL"}}
        with patch.dict(os.environ, env, clear=True):
            site = load_site()
            self.assertEqual(site.model, "gemini-3.6-flash")
            self.assertEqual(site.image_model, "gemini-3.1-flash-image")
        self.assertEqual(DEFAULT_MODEL, "gemini-3.6-flash")


class PostTests(unittest.TestCase):
    def test_fixture_posts_parse(self):
        posts = load_all_posts()
        dates = {post.date for post in posts}
        self.assertIn("2026-09-10", dates)
        self.assertIn("2026-09-09", dates)
        for post in posts:
            self.assertTrue(post.title)
            self.assertTrue(post.source)
            self.assertTrue(post.body)
            if post.header_image:
                self.assertTrue(post.header_image.startswith("assets/headers/"))

    def test_round_trip_front_matter(self):
        path = ROOT / "posts" / "2026-09-10" / "hacker-news.md"
        post = parse_post(path)
        self.assertEqual(post.slug, "hacker-news")
        self.assertEqual(post.date, "2026-09-10")
        self.assertEqual(post.header_image, "assets/headers/2026-09-10/hacker-news.png")


class FeedSkipTests(unittest.TestCase):
    def test_unreadable_feed_is_skipped(self):
        class Parsed:
            bozo = True
            entries = []
            bozo_exception = RuntimeError("nope")

        feeds = [Feed(id="nope", name="Nope", url="https://example.invalid/feed.xml")]
        with patch("digest.feeds.feedparser.parse", return_value=Parsed()):
            result = fetch_all(feeds, date(2026, 9, 10), 5)
        self.assertEqual(result, {})


class GeminiKeyTests(unittest.TestCase):
    def test_missing_key_exits(self):
        env = {k: v for k, v in os.environ.items() if k != "GEMINI_API_KEY"}
        env["GEMINI_API_KEY"] = ""
        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(SystemExit) as raised:
                require_api_key()
        self.assertIn("GEMINI_API_KEY", str(raised.exception))


class BuildTests(unittest.TestCase):
    def test_build_writes_date_pages(self):
        docs = build()
        index = (docs / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-date-picker', index)
        self.assertIn("2026-09-10", index)

        day = docs / "2026-09-10" / "index.html"
        self.assertTrue(day.is_file())
        self.assertIn("hacker-news.html", day.read_text(encoding="utf-8"))

        post = docs / "2026-09-10" / "hacker-news.html"
        html = post.read_text(encoding="utf-8")
        self.assertIn("Hacker News", html)
        self.assertIn("assets/headers/2026-09-10/hacker-news.png", html)
        self.assertIn("post-hero", html)
        self.assertTrue((docs / "assets" / "headers" / "2026-09-10" / "hacker-news.png").is_file())

        home = (docs / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="thumb"', home)
        day_html = day.read_text(encoding="utf-8")
        self.assertIn("thumb-wrap", day_html)

        dates = json.loads((docs / "dates.json").read_text(encoding="utf-8"))
        self.assertEqual(dates[0], max(dates))
        self.assertIn("2026-09-09", dates)

        self.assertTrue((docs / "dates" / "index.html").is_file())
        self.assertTrue((docs / "assets" / "style.css").is_file())
        self.assertTrue((docs / ".nojekyll").is_file())


class CliTests(unittest.TestCase):
    def test_date_after_subcommand(self):
        from digest.cli import main

        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}, clear=False):
            with self.assertRaises(SystemExit) as raised:
                main(["summarize", "--date", "2026-09-10"])
        self.assertIn("GEMINI_API_KEY", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
