import base64
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import httpx

from digest.config import DEFAULT_IMAGE_MODEL, Feed, load_site
from digest.images import (
    JPEG_MIME,
    extension_for,
    extract_image_bytes,
    generate_image,
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
TINY_JPEG = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9"


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def _status_error(code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://example.invalid")
    response = httpx.Response(code, request=request, text=f"error {code}")
    return httpx.HTTPStatusError(f"{code}", request=request, response=response)


class HeaderPromptTests(unittest.TestCase):
    def test_prompt_includes_title_and_no_text_rule(self):
        prompt = header_prompt("Models and memory", "Engineers argued about YAML.")
        self.assertIn("Models and memory", prompt)
        self.assertIn("YAML", prompt)
        self.assertIn("No text", prompt)
        self.assertIn("16:9", prompt)


class ExtractImageTests(unittest.TestCase):
    def test_interactions_output_image(self):
        payload = {"output_image": {"data": _b64(TINY_JPEG), "mime_type": "image/jpeg"}}
        self.assertEqual(extract_image_bytes(payload), TINY_JPEG)

    def test_interactions_steps(self):
        payload = {
            "steps": [
                {"type": "model_output", "content": [{"type": "image", "data": _b64(TINY_JPEG)}]}
            ]
        }
        self.assertEqual(extract_image_bytes(payload), TINY_JPEG)

    def test_generate_content_inline_data(self):
        payload = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "ok"},
                            {"inlineData": {"mimeType": "image/jpeg", "data": _b64(TINY_JPEG)}},
                        ]
                    }
                }
            ]
        }
        self.assertEqual(extract_image_bytes(payload), TINY_JPEG)

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
        self.assertEqual(extension_for(data), ".png")


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
        with patch("digest.images.generate_image", side_effect=httpx.ConnectError("nope")):
            self.assertIsNone(try_write_header(post))

    def test_relpath_defaults_to_jpg(self):
        self.assertEqual(
            header_relpath("2026-09-10", "hacker-news"),
            "assets/headers/2026-09-10/hacker-news.jpg",
        )
        self.assertEqual(
            header_relpath("2026-09-10", "hacker-news", ".png"),
            "assets/headers/2026-09-10/hacker-news.png",
        )

    def test_jpeg_bytes_saved_as_jpg_not_png(self):
        post = Post(
            slug="demo",
            title="Demo",
            date="2026-09-10",
            source="Demo",
            source_url="https://example.com",
            body="A short body.",
        )
        with tempfile.TemporaryDirectory() as tmp:
            with patch("digest.images.DOCS_DIR", Path(tmp)):
                with patch("digest.images.generate_image", return_value=TINY_JPEG):
                    rel = try_write_header(post)
            self.assertEqual(rel, "assets/headers/2026-09-10/demo.jpg")
            saved = Path(tmp) / rel
            self.assertTrue(saved.is_file())
            self.assertTrue(saved.read_bytes().startswith(b"\xff\xd8"))
            self.assertFalse((Path(tmp) / "assets/headers/2026-09-10/demo.png").exists())


class GenerateApiTests(unittest.TestCase):
    def test_generate_content_is_primary(self):
        payload = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"inlineData": {"mimeType": "image/jpeg", "data": _b64(TINY_JPEG)}}]
                    }
                }
            ]
        }
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("digest.images._generate_content_request", return_value=payload) as primary:
                with patch("digest.images._interactions_request") as fallback:
                    data = generate_image("make a header")
        self.assertEqual(data, TINY_JPEG)
        primary.assert_called_once()
        fallback.assert_not_called()

    def test_any_generate_content_error_falls_back_to_interactions(self):
        payload = {"output_image": {"data": _b64(TINY_JPEG), "mime_type": JPEG_MIME}}
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("digest.images._generate_content_request", side_effect=_status_error(400)):
                with patch("digest.images._interactions_request", return_value=payload) as fallback:
                    data = generate_image("make a header")
        self.assertEqual(data, TINY_JPEG)
        fallback.assert_called_once()

    def test_interactions_requests_jpeg_not_png(self):
        captured: dict = {}

        def fake_post(url, **kwargs):
            captured["url"] = str(url)
            captured["json"] = kwargs.get("json")
            request = httpx.Request("POST", str(url))
            return httpx.Response(
                200,
                json={"output_image": {"data": _b64(TINY_JPEG), "mime_type": JPEG_MIME}},
                request=request,
            )

        with patch("digest.images.httpx.post", side_effect=fake_post):
            from digest.images import _interactions_request

            _interactions_request("test-key", "gemini-3.1-flash-image", "prompt")
        self.assertIn("interactions", captured["url"])
        self.assertEqual(captured["json"]["response_format"]["mime_type"], "image/jpeg")
        self.assertNotEqual(captured["json"]["response_format"]["mime_type"], "image/png")

    def test_extension_rejects_mismatched_bytes(self):
        self.assertEqual(extension_for(TINY_JPEG), ".jpg")
        self.assertEqual(extension_for(TINY_PNG), ".png")
        with self.assertRaises(ValueError):
            extension_for(b"not-an-image")


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
                    return_value="assets/headers/2026-09-10/demo.jpg",
                ):
                    _summarize_feed(
                        feed,
                        date(2026, 9, 10),
                        [{"title": "A", "link": "https://example.com/a", "published": "", "summary": ""}],
                        "gemini-3.6-flash",
                        "gemini-3.1-flash-image",
                    )
        self.assertEqual(captured, ["", "assets/headers/2026-09-10/demo.jpg"])

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
