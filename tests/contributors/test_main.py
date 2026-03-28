import json

import pytest

from syslabcom_github_checks.contributors.__main__ import main

MODULE = "syslabcom_github_checks.contributors.__main__"


def test_missing_token_exits_with_code_1(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)

    with pytest.raises(SystemExit) as exc_info:
        main([])
    assert exc_info.value.code == 1


def test_dry_run_does_not_write(monkeypatch, tmp_path):
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
    monkeypatch.setattr(
        f"{MODULE}.collect", lambda **kw: []
    )
    monkeypatch.setattr(
        f"{MODULE}.OUTPUT_DIR", tmp_path / "out"
    )

    main(["--dry-run"])
    assert not (tmp_path / "out").exists()


def test_normal_run_writes_json(monkeypatch, tmp_path):
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
    monkeypatch.setattr(
        f"{MODULE}.collect", lambda **kw: []
    )
    out_dir = tmp_path / "out"
    monkeypatch.setattr(f"{MODULE}.OUTPUT_DIR", out_dir)
    monkeypatch.setattr(
        f"{MODULE}.OUTPUT_FILE", "test.json"
    )

    main([])

    path = out_dir / "test.json"
    assert path.exists()
    data = json.loads(path.read_text())
    assert data["meta"]["total_cards"] == 0
    assert data["issues"] == []
