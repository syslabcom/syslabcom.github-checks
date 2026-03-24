"""Utility functions for the contributors tool."""

from pathlib import Path


def find_project_root():
    """Walk up from this file to find the repo root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()
