# RSS Daily Digest

Daily Gemini summaries from configured RSS sources, published as blog posts on GitHub Pages. Pick a date to read that day's digests.

## What you get

- `feeds.yaml` — a starter list of data-science RSS feeds (arXiv cs.LG, Towards Data Science, KDnuggets, Hugging Face, Lil’Log, Sebastian Raschka).
- A Python pipeline that fetches new items, asks Gemini to write **one blog post per feed per day**, and builds a static site.
- GitHub Actions: a noon-UTC cron job plus a CI smoke build that **does not** call Gemini.
- GitHub Pages from the `/docs` folder on `main`.

## Architecture

```
feeds.yaml  →  digest.feeds     fetch RSS/Atom
            →  digest.gemini    one summary per feed
            →  digest.images    header PNG per post (Gemini image API)
            →  digest.posts     posts/YYYY-MM-DD/<feed-id>.md
            →  digest.site      docs/  (HTML + CSS + header images)
```

| Command | Calls Gemini? | Writes |
| --- | --- | --- |
| `python -m digest fetch` | no | `data/YYYY-MM-DD/*.json` (gitignored cache) |
| `python -m digest summarize` | yes (text + header image) | `posts/YYYY-MM-DD/*.md` and `docs/assets/headers/YYYY-MM-DD/<slug>.png` |
| `python -m digest build` | no | `docs/` |
| `python -m digest run` | yes | fetch + summarize + build |

`build` is the smoke path: it only reads markdown already in `posts/` (including the sample days committed in this repo).

## Date URLs

| URL | Page |
| --- | --- |
| `/` | Recent days + date field |
| `/YYYY-MM-DD/` | Every post from that UTC day |
| `/YYYY-MM-DD/<feed-id>.html` | One source’s post |
| `/dates/` | Index of every day that has posts |
| `/dates.json` | Machine list of dates (newest first) |

Type or pick a date in the header. If that day exists, the browser goes to `/YYYY-MM-DD/`. If not, the field reports “No digest for this date.” The date index works with JavaScript disabled.

On a GitHub project site the same paths sit under `https://<user>.github.io/<repo>/`. Links in the HTML are relative (`./`, `../`), so they work there and locally.

## Local run

Needs Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env        # then paste GEMINI_API_KEY
```

Build the site from the sample posts (no API key):

```bash
python -m digest build
python -m http.server -d docs 8000
# open http://127.0.0.1:8000/
```

Full daily pipeline (needs a key):

```bash
python -m digest run
# optional: python -m digest run --date 2026-09-10
```

Equivalent: `digest fetch`, `digest summarize`, `digest build` after `pip install -e .`.

If `GEMINI_API_KEY` is missing, `summarize` / `run` exit with instructions. A single feed that errors is skipped and logged; the rest of the run continues. If header-image generation fails for a post, a warning is logged and the text post is still published.

`python -m digest build` never calls Gemini. Sample days in `posts/` ship with lightweight placeholder PNGs under `docs/assets/headers/` so the site still has hero images offline.

## Add or remove feeds

Edit `feeds.yaml`:

```yaml
feeds:
  - id: my-feed          # used in the URL: /2026-09-10/my-feed.html
    name: Human title
    url: https://example.com/feed.xml
    homepage: https://example.com
```

`id` must be unique and filename-safe. `max_items` caps how many entries per feed are sent to Gemini.

## GEMINI_API_KEY

Never commit a key. The client reads **only** the environment (and a local `.env` via python-dotenv).

**Local:** copy `.env.example` to `.env` and set `GEMINI_API_KEY=...`. Optional: `GEMINI_MODEL=...` to override the default (`gemini-3.6-flash` in `feeds.yaml` and the client). Optional: `GEMINI_IMAGE_MODEL=...` to override the header-image model (`gemini-3.1-flash-image`, Nano Banana 2). Do not use `gemini-2.0-flash` — it is retired and returns 404.

**GitHub Actions:** repo **Settings → Secrets and variables → Actions → New repository secret**. Name it exactly `GEMINI_API_KEY`. The daily workflow refuses to start if the secret is empty. It uses `gemini-3.6-flash` for text and `gemini-3.1-flash-image` for headers unless `GEMINI_MODEL` / `GEMINI_IMAGE_MODEL` are set.

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

## Header images

After Gemini writes a post, `summarize` / `run` call Gemini again (same `GEMINI_API_KEY`) to generate a landscape 16:9 hero image. The PNG is saved at `docs/assets/headers/YYYY-MM-DD/<slug>.png` and the path is stored as `header_image` in the post’s YAML front matter. Post pages show it as a hero; day and home listings use a cropped thumbnail.

The current default image model is `gemini-3.1-flash-image` (Nano Banana 2) via the Interactions API, with `generateContent` as a fallback. Override with `GEMINI_IMAGE_MODEL` or `image_model` in `feeds.yaml`. A failed image call is a warning only — the markdown post is still written.

`python -m digest build` does not generate images. Fixture posts use committed placeholder PNGs so CI and local builds work without a key.

## Enable GitHub Pages

1. Merge to `main` (this repo already contains `docs/` from the fixture build).
2. **Settings → Pages**.
3. **Build and deployment → Source:** “Deploy from a branch”.
4. **Branch:** `main`, **folder:** `/docs`. Save.

Pages will publish `https://<user>.github.io/<repo>/`. After the first daily Action run, new days appear as new folders under `docs/`.

The daily workflow **commits** `posts/` and `docs/` back to the branch. That is the deploy. You do not need `actions/upload-pages-artifact` unless you later switch Source to “GitHub Actions”.

## GitHub Actions

- [`.github/workflows/daily.yml`](.github/workflows/daily.yml) — cron `0 12 * * *` (12:00 UTC) and **workflow_dispatch**. Installs the package, runs `python -m digest run` with `secrets.GEMINI_API_KEY` and models from `feeds.yaml` (`gemini-3.6-flash` for text, `gemini-3.1-flash-image` for headers; `gemini-2.0-flash` is retired). Commits if `posts/` or `docs/` changed (including header PNGs). Permissions: `contents: write` (and `pages: write` reserved for a future artifact deploy).
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) — on pull request and `main`: `python -m digest build` plus unit tests. No Gemini secret.

## Layout

```
feeds.yaml                 feed list + site title
posts/YYYY-MM-DD/*.md      source of truth for the blog
docs/                      GitHub Pages output (generated)
docs/assets/headers/       Gemini (or placeholder) hero images
digest/feeds.py            RSS
digest/gemini.py           Gemini REST (text)
digest/images.py           Gemini image generation for post headers
digest/posts.py            markdown posts
digest/site.py             HTML build
digest/pipeline.py         fetch / summarize / build / run
CURSOR.md                  coding conventions
```

Sample days `2026-09-09` and `2026-09-10` ship in `posts/` so Pages looks populated before the first live cron.
