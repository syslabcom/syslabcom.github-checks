"""CLI entry point for the contributors-wanted aggregator."""

import argparse
import logging

from ..github_graphql.auth import get_headers
from .collector import collect
from .config import (
    BOARDS,
    CONTRIBUTORS_LABEL,
    OUTPUT_DIR,
    OUTPUT_FILE,
    REPOSITORIES,
)
from .output import build_output, write_json

log = logging.getLogger(__name__)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Aggregate contributors-wanted issues.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and display count without writing",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        headers = get_headers()
    except ValueError as exc:
        log.error(exc)
        raise SystemExit(1)

    cards = collect(headers=headers)
    log.info("Found %d contributor cards", len(cards))

    if args.dry_run:
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / OUTPUT_FILE

    data = build_output(cards, BOARDS, REPOSITORIES, CONTRIBUTORS_LABEL)
    write_json(data, path)
    log.info("Wrote %s", path)


if __name__ == "__main__":
    main()
