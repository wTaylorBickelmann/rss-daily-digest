# Coding conventions

## Readability

- Prefer a short, named function over a comment or a nested block.
- One screen per function is a useful ceiling, not a law.
- Names should say what the thing *is* (`fetch_feed`, `write_post`, `build`).

## Modularity

Keep these areas in separate modules. Do not collapse them to save files.

| Area | Module | Responsibility |
| --- | --- | --- |
| Feeds | `digest/feeds.py` | RSS/Atom fetch, item filter, skip-on-error |
| Gemini | `digest/gemini.py` | API key check, prompt, HTTP call |
| Posts | `digest/posts.py` | Markdown + YAML front matter |
| Site | `digest/site.py` | Static HTML/CSS into `docs/` |
| Pipeline | `digest/pipeline.py` | `fetch` / `summarize` / `build` / `run` |

`python -m digest build` must work with fixture posts and **no** API key.

## Errors

- Missing `GEMINI_API_KEY` during `summarize` or `run`: exit with a clear message.
- One RSS feed or one Gemini call failing: log a warning and continue.
- Never hardcode secrets.

## Site

GitHub Pages serves committed files in `docs/`. Relative URLs only (`./`, `../`) so the same HTML works on a project site and on `python -m http.server`.
