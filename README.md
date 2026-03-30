# syslabcom-github-checks
A library to run checks and logic against github boards and issues.

## Packages

- **github_graphql** -- reusable GraphQL client for the GitHub API
- **contributors** -- CLI tool that aggregates issues matching a configured
  label from configured project boards and writes JSON output

## Installation

```
pip install -e .
```

For development (includes pytest, pre-commit, etc.):

```
pip install -e ".[dev]"
```

Requires Python 3.11+.

## Authentication

Tools that interact with the GitHub API accept a token either explicitly
or via environment variables `GITHUB_TOKEN` / `GH_TOKEN`.

## Development

Run tests:

```
pytest tests/
```

Integration tests make real API calls and require a valid GitHub token.
