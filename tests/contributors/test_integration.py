"""Integration test — real API call to Plone project 28."""

import os
import warnings

import pytest

from syslabcom_github_checks.contributors.collector import collect
from syslabcom_github_checks.github_graphql.auth import get_headers

# Temporary label override until "contributors wanted"
# exists on the board
TEST_LABEL = "31 needs: help"
TEST_BOARDS = [{"org": "plone", "project_num": 28}]
COLLECTOR = "syslabcom_github_checks.contributors.collector"

pytestmark = pytest.mark.integration

token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if not token:
    pytest.skip(
        "Requires GITHUB_TOKEN or GH_TOKEN",
        allow_module_level=True,
    )


def test_real_plone_board(monkeypatch):
    monkeypatch.setattr(f"{COLLECTOR}.BOARDS", TEST_BOARDS)
    monkeypatch.setattr(f"{COLLECTOR}.CONTRIBUTORS_LABEL", TEST_LABEL)
    headers = get_headers(token)
    cards = collect(headers=headers)
    if not cards:
        pytest.skip("Board returned no matching cards")

    for card in cards:
        assert isinstance(card.title, str)
        assert isinstance(card.number, int)
        assert card.url.startswith("https://github.com/")
        assert card.state in ("OPEN", "CLOSED")
        assert TEST_LABEL in [lbl.lower() for lbl in card.labels]

    has_start = any(c.start_date for c in cards)
    has_fix = any(c.fix_date for c in cards)
    if not has_start:
        warnings.warn("No 'Start Date' found on any card")
    if not has_fix:
        warnings.warn("No 'Fix Date' found on any card")
