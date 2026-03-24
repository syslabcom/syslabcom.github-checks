"""Configuration for the contributors-wanted aggregator."""

from .utils import find_project_root

BOARDS = [
    {
        "org": "plone",
        "project_num": 28,
    },
]

CONTRIBUTORS_LABEL = "contributors wanted"

# Allow-list of repositories. Empty = include all repos from the board.
REPOSITORIES = []

OUTPUT_DIR = find_project_root() / "output"
OUTPUT_FILE = "contributors_wanted.json"
