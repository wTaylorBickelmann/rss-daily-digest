---
title: Actions, Pages, and a reminder that YAML is still load-bearing
date: 2026-09-09
source: GitHub Blog
source_url: https://github.blog
slug: github-blog
---

GitHub’s blog spent yesterday on the unglamorous parts of shipping: Actions runners, Pages deployment, and a security note that will matter more to bot authors than to README readers.

If you run a static site from a repository, the Pages piece is the one to open. It restates the branch-versus-Actions choice without pretending they are equivalent — `/docs` on `main` is still the least moving parts if your pipeline already commits HTML.

## Stories

- [Deploying Pages from what you already committed](https://github.blog/) — Branch source, `/docs` folder, no extra artifact workflow required.
- [Workflow permissions, restated](https://github.blog/) — `contents: write` is enough to push generated posts; add `pages: write` only if you use `actions/deploy-pages`.
- [Secrets are not variables](https://github.blog/) — A gentle prod to put `GEMINI_API_KEY` in Actions secrets, not in the repo.
