"""JSON output for the contributors-wanted aggregator."""

import datetime
import json


def build_output(cards, boards, repositories):
    """Build the full JSON-serializable output dict."""
    return {
        "meta": {
            "generated_at": datetime.datetime.now().isoformat(),
            "generator": "syslabcom_github_checks.contributors",
            "boards_queried": boards,
            "repositories": repositories,
            "total_cards": len(cards),
        },
        "issues": [card.to_dict() for card in cards],
    }


def write_json(data, path):
    """Write JSON output to a file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
