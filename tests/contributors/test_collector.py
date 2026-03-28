from syslabcom_github_checks.contributors.collector import collect

MODULE = "syslabcom_github_checks.contributors.collector"

# A minimal issue node that passes all filters
ISSUE_NODE = {
    "fieldValues": {"nodes": []},
    "content": {
        "__typename": "Issue",
        "title": "Help wanted",
        "number": 1,
        "url": "https://github.com/plone/volto/issues/1",
        "state": "OPEN",
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-02T00:00:00Z",
        "author": {"login": "alice"},
        "assignees": {"nodes": []},
        "labels": {"nodes": [{"name": "contributors wanted"}]},
        "repository": {"nameWithOwner": "plone/volto"},
    },
}

PR_NODE = {
    "fieldValues": {"nodes": []},
    "content": {"__typename": "PullRequest"},
}

WRONG_LABEL_NODE = {
    "fieldValues": {"nodes": []},
    "content": {
        "__typename": "Issue",
        "title": "No label match",
        "number": 2,
        "url": "https://github.com/plone/volto/issues/2",
        "state": "OPEN",
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-02T00:00:00Z",
        "author": {"login": "bob"},
        "assignees": {"nodes": []},
        "labels": {"nodes": [{"name": "bug"}]},
        "repository": {"nameWithOwner": "plone/volto"},
    },
}

BOARDS = [{"org": "plone", "project_num": 28}]


def test_collect_returns_matching_issue(monkeypatch, fake_headers):
    def fake_query_all(query, variables, path, *, headers=None):
        return [ISSUE_NODE]

    monkeypatch.setattr(f"{MODULE}.query_graphql_all", fake_query_all)
    monkeypatch.setattr(f"{MODULE}.BOARDS", BOARDS)

    cards = collect(headers=fake_headers)
    assert len(cards) == 1
    assert cards[0].title == "Help wanted"
    assert cards[0].key == "plone/volto#1"


def test_collect_skips_prs_and_wrong_labels(monkeypatch, fake_headers):
    def fake_query_all(query, variables, path, *, headers=None):
        return [PR_NODE, WRONG_LABEL_NODE, ISSUE_NODE]

    monkeypatch.setattr(f"{MODULE}.query_graphql_all", fake_query_all)
    monkeypatch.setattr(f"{MODULE}.BOARDS", BOARDS)

    cards = collect(headers=fake_headers)
    # Only ISSUE_NODE passes both filters
    assert len(cards) == 1
    assert cards[0].title == "Help wanted"


def test_collect_skips_failed_board(monkeypatch, fake_headers):
    def fake_query_all(query, variables, path, *, headers=None):
        raise RuntimeError("API error")

    monkeypatch.setattr(f"{MODULE}.query_graphql_all", fake_query_all)
    monkeypatch.setattr(f"{MODULE}.BOARDS", BOARDS)

    cards = collect(headers=fake_headers)
    assert cards == []


def test_collect_filters_by_repo_allowlist(monkeypatch, fake_headers):
    def fake_query_all(query, variables, path, *, headers=None):
        return [ISSUE_NODE]

    monkeypatch.setattr(f"{MODULE}.query_graphql_all", fake_query_all)
    # ISSUE_NODE is plone/volto, allow-list only plone/plone
    monkeypatch.setattr(f"{MODULE}.REPOSITORIES", ["plone/plone"])
    monkeypatch.setattr(f"{MODULE}.BOARDS", BOARDS)

    cards = collect(headers=fake_headers)
    assert cards == []
