import pytest

from syslabcom_github_checks.github_graphql.client import (
    query_graphql,
    query_graphql_all,
)
from tests.conftest import _FakeResponse

MODULE = "syslabcom_github_checks.github_graphql.client"


@pytest.mark.parametrize(
    "payload, path, expected",
    [
        (
            {"data": {"org": {"name": "plone"}}},
            "data.org.name",
            "plone",
        ),
        (
            {
                "data": {"org": {"name": "plone"}},
                "errors": [{"message": "warn"}],
            },
            "data.org.name",
            "plone",
        ),
    ],
    ids=["simple-success", "partial-errors-still-returns-data"],
)
def test_query_graphql_success(
    monkeypatch, fake_headers, payload, path, expected
):
    def fake_post(_url, headers=None, json=None, timeout=None):
        return _FakeResponse(payload)

    monkeypatch.setattr(f"{MODULE}.requests.post", fake_post)
    result = query_graphql("query {}", {}, path, headers=fake_headers)
    assert result == expected


def test_query_graphql_http_error(monkeypatch, fake_headers):
    def fake_post(_url, headers=None, json=None, timeout=None):
        return _FakeResponse({"message": "bad"}, status_code=403)

    monkeypatch.setattr(f"{MODULE}.requests.post", fake_post)
    with pytest.raises(RuntimeError, match="HTTP 403"):
        query_graphql("query {}", {}, "data", headers=fake_headers)


# --- query_graphql_all tests ---


def test_query_graphql_all_single_page(monkeypatch, fake_headers):
    payload = {
        "data": {
            "items": {
                "nodes": [{"id": 1}, {"id": 2}],
                "pageInfo": {
                    "hasNextPage": False,
                    "endCursor": None,
                },
            }
        }
    }

    def fake_post(_url, headers=None, json=None, timeout=None):
        return _FakeResponse(payload)

    monkeypatch.setattr(f"{MODULE}.requests.post", fake_post)
    result = query_graphql_all(
        "query {}", {}, "data.items", headers=fake_headers
    )
    assert result == [{"id": 1}, {"id": 2}]


def test_query_graphql_all_multiple_pages(monkeypatch, fake_headers):
    pages = [
        {
            "data": {
                "items": {
                    "nodes": [{"id": 1}],
                    "pageInfo": {
                        "hasNextPage": True,
                        "endCursor": "cursor_1",
                    },
                }
            }
        },
        {
            "data": {
                "items": {
                    "nodes": [{"id": 2}],
                    "pageInfo": {
                        "hasNextPage": False,
                        "endCursor": None,
                    },
                }
            }
        },
    ]
    received_cursors = []

    def fake_post(_url, headers=None, json=None, timeout=None):
        cursor = json["variables"].get("itemsCursor")
        received_cursors.append(cursor)
        return _FakeResponse(pages[len(received_cursors) - 1])

    monkeypatch.setattr(f"{MODULE}.requests.post", fake_post)
    result = query_graphql_all(
        "query {}", {}, "data.items", headers=fake_headers
    )
    assert result == [{"id": 1}, {"id": 2}]
    assert received_cursors == [None, "cursor_1"]


def test_query_graphql_all_http_error(monkeypatch, fake_headers):
    def fake_post(_url, headers=None, json=None, timeout=None):
        return _FakeResponse({"message": "bad"}, status_code=500)

    monkeypatch.setattr(f"{MODULE}.requests.post", fake_post)
    with pytest.raises(RuntimeError, match="HTTP 500"):
        query_graphql_all("query {}", {}, "data.items", headers=fake_headers)
