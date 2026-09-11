"""Thin Gemini REST client. No keys in code — only GEMINI_API_KEY from the env."""

from __future__ import annotations

import re

import httpx

from digest.config import DEFAULT_MODEL, gemini_api_key

MISSING_KEY_MESSAGE = """\
GEMINI_API_KEY is not set.

Local: copy .env.example to .env and paste your key, or export GEMINI_API_KEY.
GitHub Actions: Settings → Secrets and variables → Actions → New repository secret
named GEMINI_API_KEY.
"""


def require_api_key() -> str:
    key = gemini_api_key()
    if not key:
        raise SystemExit(MISSING_KEY_MESSAGE)
    return key


def digest_prompt(feed_name: str, day: str, items: list[dict]) -> str:
    blocks = []
    for index, item in enumerate(items, 1):
        blocks.append(
            f"{index}. {item['title']}\n"
            f"   URL: {item['link']}\n"
            f"   Date: {item.get('published') or 'unknown'}\n"
            f"   Excerpt: {item.get('summary') or ''}"
        )
    catalog = "\n\n".join(blocks)
    return f"""Write a readable blog post digest of these RSS items from {feed_name} for {day} (UTC).

Rules:
- Start with a single markdown H1 title (not a generic "Daily Digest").
- Then 2–4 short paragraphs of synthesis: what mattered and why.
- Then a markdown list of the items you cover, each a link to the original URL
  with a one-sentence gloss.
- Only use the items below. Do not invent stories, quotes, or URLs.
- Neutral, specific, no hype or emojis.

Items:

{catalog}
"""


def generate(prompt: str, model: str | None = None) -> str:
    key = require_api_key()
    model = (model or DEFAULT_MODEL).strip() or DEFAULT_MODEL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 4096},
    }
    response = httpx.post(url, params={"key": key}, json=payload, timeout=90)
    response.raise_for_status()
    data = response.json()
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected Gemini response: {data}") from exc
    return _strip_fences(text)


def split_title(markdown: str) -> tuple[str, str]:
    lines = markdown.strip().splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip(), "\n".join(lines[1:]).strip()
    return "", markdown.strip()


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:markdown|md)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()
