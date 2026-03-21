import pytest

from syslabcom_github_checks.github_graphql.utils import j_get


@pytest.mark.parametrize(
    "path, data, expected",
    [
        ("a.b", {"a": {"b": 42}}, 42),
        ("a.b.c", {"a": {"b": {"c": "deep"}}}, "deep"),
        ("items[0].name", {"items": [{"name": "first"}]}, "first"),
        ("missing.path", {"a": 1}, None),
        ("a", None, None),
    ],
    ids=[
        "nested-key",
        "deeply-nested",
        "array-index",
        "missing-path",
        "none-data",
    ],
)
def test_j_get(path, data, expected):
    assert j_get(path, data) == expected
