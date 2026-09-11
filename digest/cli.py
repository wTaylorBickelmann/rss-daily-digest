"""CLI: python -m digest fetch|summarize|build|run"""

from __future__ import annotations

import argparse
import logging
import sys

from digest.config import parse_date
from digest import pipeline


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="digest",
        description="Fetch RSS, summarize with Gemini, build the GitHub Pages site.",
    )
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument(
        "--date",
        help="UTC date YYYY-MM-DD (default: today UTC). Ignored by build.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("fetch", parents=[shared], help="Download RSS items for the date")
    sub.add_parser("summarize", parents=[shared], help="Write Gemini posts from fetched items")
    sub.add_parser("build", parents=[shared], help="Build docs/ from posts/ (no Gemini call)")
    sub.add_parser("run", parents=[shared], help="fetch + summarize + build")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    day = parse_date(args.date)

    if args.command == "fetch":
        pipeline.fetch(day)
    elif args.command == "summarize":
        pipeline.summarize(day)
    elif args.command == "build":
        pipeline.build()
    elif args.command == "run":
        pipeline.run(day)
    else:
        parser.error(f"unknown command {args.command}")


if __name__ == "__main__":
    main(sys.argv[1:])
