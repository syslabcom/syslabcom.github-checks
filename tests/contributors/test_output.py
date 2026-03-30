import json

from syslabcom_github_checks.contributors.models import (
    ContributorCard,
)
from syslabcom_github_checks.contributors.output import (
    build_output,
    write_json,
)

BOARDS = [{"org": "plone", "project_num": 28}]
REPOSITORIES = ["plone/volto"]
LABEL = "contributors wanted"

CARD = ContributorCard(
    key="plone/volto#1",
    title="Fix bug",
    url="https://github.com/plone/volto/issues/1",
    repository="plone/volto",
    number=1,
    state="OPEN",
    board_status="In Progress",
    labels=["contributors wanted"],
    author="alice",
    assignees=["bob"],
    created_at="2026-01-01T00:00:00Z",
    updated_at="2026-01-02T00:00:00Z",
    project_name="plone/28",
)


def test_build_output():
    result = build_output([CARD], BOARDS, REPOSITORIES, LABEL)
    assert "meta" in result
    assert "issues" in result
    assert result["meta"]["total_cards"] == 1
    assert result["meta"]["boards_queried"] == BOARDS
    assert result["meta"]["repositories"] == REPOSITORIES
    assert result["meta"]["label"] == LABEL
    assert "generated_at" in result["meta"]
    assert result["issues"][0]["key"] == "plone/volto#1"


def test_write_json(tmp_path):
    data = {"test": "value"}
    path = tmp_path / "out.json"
    write_json(data, path)
    with open(path, encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == data
