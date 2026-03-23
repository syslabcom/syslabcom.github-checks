"""Configuration for the contributors-wanted aggregator."""

BOARDS = [
    {
        "org": "plone",
        "project_num": 28,
    },
]

CONTRIBUTORS_LABEL = "contributors wanted"

# Allow-list of repositories. Empty = include all repos from the board.
REPOSITORIES = []

OUTPUT_FILE = "contributors_wanted.json"
