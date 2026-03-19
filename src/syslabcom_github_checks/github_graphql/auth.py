import os


def get_headers(token=None):
    """Resolve a GitHub token and return auth headers."""
    token = (
        token
        or os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
    )
    if not token:
        raise ValueError(
            "GitHub token required: pass token argument,"
            " or set GITHUB_TOKEN / GH_TOKEN env var"
        )
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
