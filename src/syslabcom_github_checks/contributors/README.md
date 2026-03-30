# contributors

CLI tool that fetches issues matching a configured label from GitHub
ProjectV2 boards and writes them as JSON.

## Usage

```
contributors-wanted [--dry-run] [--verbose]
```

- `--dry-run` -- fetch and log the card count without writing output
- `--verbose` -- enable debug logging

Output is written to `output/contributors_wanted.json` relative to the
project root.

## Configuration

Edit `config.py` to configure the tool:

```python
# Boards to fetch from
BOARDS = [
    {"org": "plone", "project_num": 28},
]

# Label to filter issues by (case-insensitive)
CONTRIBUTORS_LABEL = "contributors wanted"

# Repository allow-list. Empty = include all repos from the board.
REPOSITORIES = []
```

## Output format

```json
{
  "meta": {
    "generated_at": "2026-03-30T10:00:00",
    "generator": "syslabcom_github_checks.contributors",
    "boards_queried": [{"org": "plone", "project_num": 28}],
    "repositories": [],
    "label": "contributors wanted",
    "total_cards": 4
  },
  "issues": [
    {
      "key": "plone/volto#1234",
      "title": "Add dark mode support",
      "url": "https://github.com/plone/volto/issues/1234",
      "repository": "plone/volto",
      "number": 1234,
      "state": "OPEN",
      "board_status": "In Progress",
      "labels": ["contributors wanted"],
      "author": "davisagli",
      "assignees": [],
      "created_at": "2026-01-15T10:00:00Z",
      "updated_at": "2026-03-10T08:00:00Z",
      "start_date": null,
      "fix_date": null,
      "project_name": "plone/28"
    }
  ]
}
```
