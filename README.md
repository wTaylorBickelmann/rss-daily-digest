# RSS Daily Digest

Daily Gemini summaries from configured RSS sources, published as blog posts on GitHub Pages. Pick a date to read that day's digests.

## What you get

- `feeds.yaml` — a starter list of tech, news, and research RSS feeds.
- A Python pipeline that fetches new items, asks Gemini to write **one blog post per feed per day**, and builds a static site.
- GitHub Actions: a noon-UTC cron job plus a CI smoke build that **does not** call Gemini.
- GitHub Pages from the `/docs` folder on `main`.

## Architecture

```
feeds.yaml  →  digest.feeds     fetch RSS/Atom
            →  digest.gemini    one summary per feed
            →  digest.posts     posts/YYYY-MM-DD/<feed-id>.md
            →  digest.site      docs/  (HTML + CSS)
```

| Command | Calls Gemini? | Writes |
| --- | --- | --- |
| `python -m digest fetch` | no | `data/YYYY-MM-DD/*.json` (gitignored cache) |
| `python -m digest summarize` | yes | `posts/YYYY-MM-DD/*.md` |
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

If `GEMINI_API_KEY` is missing, `summarize` / `run` exit with instructions. A single feed that errors is skipped and logged; the rest of the run continues.

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

**Local:** copy `.env.example` to `.env` and set `GEMINI_API_KEY=...`. Optional: `GEMINI_MODEL=gemini-2.5-flash`.

**GitHub Actions:** repo **Settings → Secrets and variables → Actions → New repository secret**. Name it exactly `GEMINI_API_KEY`. The daily workflow refuses to start if the secret is empty.

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

## Enable GitHub Pages

1. Merge to `main` (this repo already contains `docs/` from the fixture build).
2. **Settings → Pages**.
3. **Build and deployment → Source:** “Deploy from a branch”.
4. **Branch:** `main`, **folder:** `/docs`. Save.

Pages will publish `https://<user>.github.io/<repo>/`. After the first daily Action run, new days appear as new folders under `docs/`.

The daily workflow **commits** `posts/` and `docs/` back to the branch. That is the deploy. You do not need `actions/upload-pages-artifact` unless you later switch Source to “GitHub Actions”.

## GitHub Actions

- [`.github/workflows/daily.yml`](.github/workflows/daily.yml) — cron `0 12 * * *` (12:00 UTC) and **workflow_dispatch**. Installs the package, runs `python -m digest run` with `secrets.GEMINI_API_KEY`, commits if `posts/` or `docs/` changed. Permissions: `contents: write` (and `pages: write` reserved for a future artifact deploy).
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) — on pull request and `main`: `python -m digest build` plus unit tests. No Gemini secret.

## Layout

```
feeds.yaml                 feed list + site title
posts/YYYY-MM-DD/*.md      source of truth for the blog
docs/                      GitHub Pages output (generated)
digest/feeds.py            RSS
digest/gemini.py           Gemini REST
digest/posts.py            markdown posts
digest/site.py             HTML build
digest/pipeline.py         fetch / summarize / build / run
CURSOR.md                  coding conventions
```

Sample days `2026-09-09` and `2026-09-10` ship in `posts/` so Pages looks populated before the first live cron.
