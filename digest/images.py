"""Gemini header images for digest posts.

Uses the current Nano Banana image models (Gemini 3.1 Flash Image) via the
Interactions API, with generateContent as a fallback. Same GEMINI_API_KEY as
text summaries. Failures are returned as None so the text post still publishes.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import os
import struct
import zlib
from pathlib import Path

import httpx

from digest.config import DEFAULT_IMAGE_MODEL, DOCS_DIR
from digest.gemini import require_api_key
from digest.posts import Post

log = logging.getLogger(__name__)

INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
GENERATE_CONTENT_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
API_REVISION = "2026-05-20"
ASPECT_RATIO = "16:9"
IMAGE_SIZE = "1K"
HEADERS_PREFIX = "assets/headers"

# Warm editorial swatches used for offline fixture placeholders.
_PLACEHOLDER_COLORS = (
    (140, 47, 13),
    (92, 83, 72),
    (26, 23, 20),
    (168, 112, 58),
    (74, 92, 78),
    (110, 70, 90),
)


def header_relpath(day: str, slug: str) -> str:
    return f"{HEADERS_PREFIX}/{day}/{slug}.png"


def header_file(day: str, slug: str) -> Path:
    return DOCS_DIR / header_relpath(day, slug)


def image_model() -> str:
    return (os.environ.get("GEMINI_IMAGE_MODEL") or DEFAULT_IMAGE_MODEL).strip() or DEFAULT_IMAGE_MODEL


def header_prompt(title: str, excerpt: str) -> str:
    blurb = " ".join((excerpt or "").split())[:400]
    return (
        "Create a clean editorial header image that fits this blog post.\n"
        "Landscape 16:9, magazine photography or conceptual illustration, "
        "muted paper-and-ink palette (warm cream, dark brown, terracotta).\n"
        "No text, logos, watermarks, captions, or UI chrome in the image "
        "unless necessary.\n\n"
        f"Title: {title.strip()}\n\n"
        f"Excerpt: {blurb}"
    )


def try_write_header(post: Post, model: str | None = None) -> str | None:
    """Generate and save a header image. Returns the site-relative path, or None."""
    prompt = header_prompt(post.title, post.excerpt(limit=360))
    try:
        png = generate_png(prompt, model)
    except (httpx.HTTPError, RuntimeError, ValueError, OSError) as exc:
        log.warning("Header image failed for %s: %s", post.slug, exc)
        return None
    path = save_png(post.date, post.slug, png)
    rel = header_relpath(post.date, post.slug)
    log.info("Wrote header %s", path)
    return rel


def generate_png(prompt: str, model: str | None = None) -> bytes:
    key = require_api_key()
    model = (model or image_model()).strip() or DEFAULT_IMAGE_MODEL
    try:
        payload = _interactions_request(key, model, prompt)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code not in {404, 405, 501}:
            raise
        log.warning(
            "Interactions image API returned %s; trying generateContent",
            exc.response.status_code,
        )
        payload = _generate_content_request(key, model, prompt)
    return extract_image_bytes(payload)


def save_png(day: str, slug: str, png: bytes) -> Path:
    path = header_file(day, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    return path


def extract_image_bytes(payload: dict) -> bytes:
    """Pull PNG/JPEG bytes from an Interactions or generateContent JSON body."""
    image = payload.get("output_image")
    if isinstance(image, dict) and image.get("data"):
        return _decode_image(image["data"])

    for step in payload.get("steps") or []:
        found = _image_in_content(step.get("content") if isinstance(step, dict) else None)
        if found:
            return found

    for candidate in payload.get("candidates") or []:
        content = candidate.get("content") if isinstance(candidate, dict) else None
        if not isinstance(content, dict):
            continue
        found = _image_in_content(content.get("parts"))
        if found:
            return found

    raise RuntimeError(f"No image in Gemini response: {list(payload)}")


def write_placeholder_png(path: Path, seed: str) -> Path:
    """Tiny landscape PNG so fixture posts have a header without calling Gemini."""
    index = int(hashlib.sha1(seed.encode("utf-8")).hexdigest(), 16)
    ink = _PLACEHOLDER_COLORS[index % len(_PLACEHOLDER_COLORS)]
    paper = (243, 234, 215)
    accent = _PLACEHOLDER_COLORS[(index // len(_PLACEHOLDER_COLORS)) % len(_PLACEHOLDER_COLORS)]
    png = _landscape_placeholder(1280, 720, paper, ink, accent)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    return path


def _interactions_request(key: str, model: str, prompt: str) -> dict:
    payload = {
        "model": model,
        "input": [{"type": "text", "text": prompt}],
        "response_format": {
            "type": "image",
            "mime_type": "image/png",
            "aspect_ratio": ASPECT_RATIO,
            "image_size": IMAGE_SIZE,
        },
    }
    headers = {
        "x-goog-api-key": key,
        "Content-Type": "application/json",
        "Api-Revision": API_REVISION,
    }
    response = httpx.post(INTERACTIONS_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def _generate_content_request(key: str, model: str, prompt: str) -> dict:
    url = GENERATE_CONTENT_URL.format(model=model)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": ASPECT_RATIO},
        },
    }
    response = httpx.post(url, params={"key": key}, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def _image_in_content(items: object) -> bytes | None:
    if not isinstance(items, list):
        return None
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("data") and item.get("type") in {None, "image"}:
            return _decode_image(item["data"])
        inline = item.get("inlineData") or item.get("inline_data")
        if isinstance(inline, dict) and inline.get("data"):
            return _decode_image(inline["data"])
        image = item.get("image")
        if isinstance(image, dict) and image.get("data"):
            return _decode_image(image["data"])
    return None


def _decode_image(data: str) -> bytes:
    raw = base64.b64decode(data)
    if not raw:
        raise ValueError("Empty image payload")
    return raw


def _landscape_placeholder(
    width: int,
    height: int,
    paper: tuple[int, int, int],
    ink: tuple[int, int, int],
    accent: tuple[int, int, int],
) -> bytes:
    field = _mix(paper, ink, 0.22)
    gutter = max(width // 8, 24)
    top = max(height // 9, 16)
    foot = max(height // 7, 20)
    rows: list[bytes] = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            if x < gutter:
                color = ink if y < height - foot else accent
            elif y < top:
                color = _mix(ink, paper, y / top)
            elif y > height - foot:
                color = accent if y > height - foot + 4 else _mix(field, accent, 0.55)
            else:
                color = field
            row.extend(color)
        rows.append(b"\x00" + bytes(row))
    return _png_rgb(width, height, b"".join(rows))


def _mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = min(max(t, 0.0), 1.0)
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def _png_rgb(width: int, height: int, raw: bytes) -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
