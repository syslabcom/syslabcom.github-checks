import pytest

from syslabcom_github_checks.github_graphql.auth import get_headers


@pytest.mark.parametrize(
    "token_arg, env_vars, expected_token",
    [
        ("explicit-tok", {}, "explicit-tok"),
        (None, {"GITHUB_TOKEN": "env-tok"}, "env-tok"),
        (None, {"GH_TOKEN": "gh-tok"}, "gh-tok"),
        (
            None,
            {"GITHUB_TOKEN": "first", "GH_TOKEN": "second"},
            "first",
        ),
    ],
    ids=[
        "explicit-token",
        "GITHUB_TOKEN-env",
        "GH_TOKEN-fallback",
        "GITHUB_TOKEN-takes-precedence",
    ],
)
def test_get_headers_resolves_token(
    monkeypatch, token_arg, env_vars, expected_token
):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    for key, val in env_vars.items():
        monkeypatch.setenv(key, val)

    headers = get_headers(token=token_arg)
    assert headers["Authorization"] == f"Bearer {expected_token}"
    assert headers["Content-Type"] == "application/json"


def test_get_headers_no_token_raises(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    with pytest.raises(ValueError, match="GitHub token required"):
        get_headers()
