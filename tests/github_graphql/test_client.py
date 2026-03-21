import pytest

from syslabcom_github_checks.github_graphql.client import query_graphql
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
    result = query_graphql(
        "query {}", {}, path, headers=fake_headers
    )
    assert result == expected


def test_query_graphql_http_error(monkeypatch, fake_headers):
    def fake_post(_url, headers=None, json=None, timeout=None):
        return _FakeResponse({"message": "bad"}, status_code=403)

    monkeypatch.setattr(f"{MODULE}.requests.post", fake_post)
    with pytest.raises(RuntimeError, match="HTTP 403"):
        query_graphql("query {}", {}, "data", headers=fake_headers)
