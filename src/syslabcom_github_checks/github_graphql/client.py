import logging

import requests

from .auth import get_headers
from .utils import j_get

log = logging.getLogger(__name__)

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def query_graphql(query, variables, path, *, headers=None):
    """Execute a single GraphQL request, return data at path."""
    if headers is None:
        headers = get_headers()

    response = requests.post(
        GITHUB_GRAPHQL_URL,
        headers=headers,
        json={"query": query, "variables": variables},
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"HTTP {response.status_code}: {response.text}"
        )

    data = response.json()
    if "errors" in data:
        log.warning("GraphQL errors: %s", data["errors"])

    return j_get(path, data)
