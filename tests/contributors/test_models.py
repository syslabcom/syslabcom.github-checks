import pytest

from syslabcom_github_checks.contributors.models import (
    ContributorCard,
)


def test_to_dict():
    card = ContributorCard(
        key="plone/volto#1",
        title="Fix bug",
        url="https://github.com/plone/volto/issues/1",
        repository="plone/volto",
        number=1,
        state="OPEN",
        board_status="In Progress",
        labels=["bug"],
        author="alice",
        assignees=["bob"],
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-02T00:00:00Z",
        start_date="2026-01-01",
        fix_date="2026-02-01",
        project_name="Plone Contributors",
    )
    result = card.to_dict()
    assert result["key"] == "plone/volto#1"
    assert result["title"] == "Fix bug"
    assert result["labels"] == ["bug"]
    assert result["board_status"] == "In Progress"
    assert len(result) == 15


def test_from_graphql():
    node = {
        "fieldValues": {
            "nodes": [
                {
                    "__typename": (
                        "ProjectV2ItemFieldSingleSelectValue"
                    ),
                    "name": "In Progress",
                    "field": {"name": "Status"},
                },
                {
                    "__typename": "ProjectV2ItemFieldDateValue",
                    "date": "2026-01-20",
                    "field": {"name": "Start Date"},
                },
                {
                    "__typename": "ProjectV2ItemFieldDateValue",
                    "date": "2026-04-01",
                    "field": {"name": "Fix Date"},
                },
            ]
        },
        "content": {
            "__typename": "Issue",
            "title": "Add dark mode",
            "number": 42,
            "url": "https://github.com/plone/volto/issues/42",
            "state": "OPEN",
            "createdAt": "2026-01-15T10:00:00Z",
            "updatedAt": "2026-03-10T08:00:00Z",
            "author": {"login": "alice"},
            "assignees": {"nodes": [{"login": "bob"}]},
            "labels": {
                "nodes": [
                    {"name": "contributors wanted"},
                    {"name": "frontend"},
                ]
            },
            "repository": {"nameWithOwner": "plone/volto"},
        },
    }
    card = ContributorCard.from_graphql(node, "Plone Board")
    assert card.key == "plone/volto#42"
    assert card.title == "Add dark mode"
    assert card.repository == "plone/volto"
    assert card.number == 42
    assert card.state == "OPEN"
    assert card.board_status == "In Progress"
    assert card.labels == ["contributors wanted", "frontend"]
    assert card.author == "alice"
    assert card.assignees == ["bob"]
    assert card.start_date == "2026-01-20"
    assert card.fix_date == "2026-04-01"
    assert card.project_name == "Plone Board"


def test_from_graphql_missing_fields():
    node = {
        "fieldValues": {"nodes": []},
        "content": {
            "__typename": "Issue",
            "title": "Minimal issue",
            "number": 7,
            "url": "https://github.com/plone/plone.classicui/issues/7",
            "state": "CLOSED",
            "createdAt": "2023-08-30T13:01:18Z",
            "updatedAt": "2025-03-12T14:37:40Z",
            "author": {"login": "MrTango"},
            "assignees": {"nodes": []},
            "labels": {"nodes": []},
            "repository": {
                "nameWithOwner": "plone/plone.classicui"
            },
        },
    }
    card = ContributorCard.from_graphql(node, "Plone Board")
    assert card.board_status is None
    assert card.start_date is None
    assert card.fix_date is None
    assert card.labels == []
    assert card.assignees == []
