---
title: Notes on evals, feeds, and writing with models that can see the links
date: 2026-09-09
source: Simon Willison’s Weblog
source_url: https://simonwillison.net
slug: simon-willison
---

A dense day even by this weblog’s standards: one post on evaluation harnesses, one on RSS as an API, and a shorter note about prompting models to quote URLs they were actually given.

The RSS piece is the one that belongs in this project’s lineage. Treat feeds as structured input, keep the model on a short leash, and store the prose in git so a bad generation is a revert, not a mystery.

## Stories

- [RSS is an API you already have](https://simonwillison.net/) — Fetch, cap the item count, and refuse to invent URLs.
- [Evals for summaries](https://simonwillison.net/) — Cheap checks: did every listed link appear in the source items?
- [Grounding without retrieval theater](https://simonwillison.net/) — Sometimes the “index” is twelve feed entries in a prompt.
