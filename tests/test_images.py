import base64
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import httpx

from digest.config import DEFAULT_IMAGE_MODEL, Feed, load_site
from digest.images import (
    extract_image_bytes,
    generate_png,
    header_prompt,
    header_relpath,
    try_write_header,
    write_placeholder_png,
)
from digest.pipeline import _summarize_feed
from digest.posts import Post


TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def _b64(raw: bytes = TINY_PNG) -> str:
    return base64.b64encode(raw).decode("ascii")


class HeaderPromptTests(unittest.TestCase):
    def test_prompt_includes_title_and_no_text_rule(self):
        prompt = header_prompt("Models and memory", "Engineers argued about YAML.")
        self.assertIn("Models and memory", prompt)
        self.assertIn("YAML", prompt)
        self.assertIn("No text", prompt)
        self.assertIn("16:9", prompt)


class ExtractImageTests(unittest.TestCase):
    def test_interactions_output_image(self):
        payload = {"output_image": {"data": _b64(), "mime_type": "image/png"}}
        self.assertEqual(extract_image_bytes(payload), TINY_PNG)

    def test_interactions_steps(self):
        payload = {
            "steps": [
                {"type": "model_output", "content": [{"type": "image", "data": _b64()}]}
            ]
        }
        self.assertEqual(extract_image_bytes(payload), TINY_PNG)

    def test_generate_content_inline_data(self):
        payload = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "ok"},
                            {"inlineData": {"mimeType": "image/png", "data": _b64()}},
                        ]
                    }
                }
            ]
        }
        self.assertEqual(extract_image_bytes(payload), TINY_PNG)

    def test_missing_image_raises(self):
        with self.assertRaises(RuntimeError):
            extract_image_bytes({"candidates": []})


class PlaceholderTests(unittest.TestCase):
    def test_placeholder_is_png(self):
        path = Path("/tmp/digest-header-placeholder.png")
        write_placeholder_png(path, "2026-09-10/hacker-news")
        data = path.read_bytes()
        self.assertTrue(data.startswith(b"\x89PNG"))
        self.assertGreater(len(data), 32)


class TryWriteHeaderTests(unittest.TestCase):
    def test_http_error_returns_none(self):
        post = Post(
            slug="demo",
            title="Demo",
            date="2026-09-10",
            source="Demo",
            source_url="https://example.com",
            body="A short body.",
        )
        with patch("digest.images.generate_png", side_effect=httpx.ConnectError("nope")):
            self.assertIsNone(try_write_header(post))

    def test_relpath(self):
        self.assertEqual(
            header_relpath("2026-09-10", "hacker-news"),
            "assets/headers/2026-09-10/hacker-news.png",
        )


class GenerateFallbackTests(unittest.TestCase):
    def test_404_falls_back_to_generate_content(self):
        missing = httpx.Response(404, request=httpx.Request("POST", "https://example.invalid"))
        err = httpx.HTTPStatusError("404", request=missing.request, response=missing)
        payload = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"inlineData": {"mimeType": "image/png", "data": _b64()}}]
                    }
                }
            ]
        }
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("digest.images._interactions_request", side_effect=err):
                with patch("digest.images._generate_content_request", return_value=payload):
                    png = generate_png("make a header")
        self.assertEqual(png, TINY_PNG)


class ConfigImageModelTests(unittest.TestCase):
    def test_default_image_model(self):
        env = {k: v for k, v in __import__("os").environ.items() if k != "GEMINI_IMAGE_MODEL"}
        with patch.dict("os.environ", env, clear=True):
            self.assertEqual(load_site().image_model, "gemini-3.1-flash-image")
        self.assertEqual(DEFAULT_IMAGE_MODEL, "gemini-3.1-flash-image")


class SummarizeHeaderTests(unittest.TestCase):
    def test_header_success_rewrites_front_matter(self):
        captured: list[str] = []

        def fake_write(post: Post) -> Path:
            captured.append(post.header_image)
            return Path("/tmp/post.md")

        feed = Feed(id="demo", name="Demo", url="https://example.com/feed", homepage="https://example.com")
        with patch("digest.pipeline.generate", return_value="# Hello\n\nBody of the digest."):
            with patch("digest.pipeline.write_post", side_effect=fake_write):
                with patch(
                    "digest.pipeline.try_write_header",
                    return_value="assets/headers/2026-09-10/demo.png",
                ):
                    _summarize_feed(
                        feed,
                        date(2026, 9, 10),
                        [{"title": "A", "link": "https://example.com/a", "published": "", "summary": ""}],
                        "gemini-3.6-flash",
                        "gemini-3.1-flash-image",
                    )
        self.assertEqual(captured, ["", "assets/headers/2026-09-10/demo.png"])

    def test_header_failure_still_writes_post(self):
        captured: list[Post] = []

        def fake_write(post: Post) -> Path:
            captured.append(post)
            return Path("/tmp/post.md")

        feed = Feed(id="demo", name="Demo", url="https://example.com/feed")
        with patch("digest.pipeline.generate", return_value="# Hello\n\nBody of the digest."):
            with patch("digest.pipeline.write_post", side_effect=fake_write):
                with patch("digest.pipeline.try_write_header", return_value=None):
                    path = _summarize_feed(
                        feed,
                        date(2026, 9, 10),
                        [{"title": "A", "link": "https://example.com/a", "published": "", "summary": ""}],
                        "gemini-3.6-flash",
                        "gemini-3.1-flash-image",
                    )
        self.assertEqual(path, Path("/tmp/post.md"))
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0].header_image, "")
        self.assertEqual(captured[0].title, "Hello")


if __name__ == "__main__":
    unittest.main()
