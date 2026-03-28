import logging
import time

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
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")

    data = response.json()
    if "errors" in data:
        log.warning("GraphQL errors: %s", data["errors"])

    return j_get(path, data)


def query_graphql_all(query, variables, path, *, headers=None, delay_sec=0.0):
    """Paginated GraphQL fetch, returns all nodes."""
    if headers is None:
        headers = get_headers()

    all_nodes = []
    cursor = None

    while True:
        variables["itemsCursor"] = cursor

        response = requests.post(
            GITHUB_GRAPHQL_URL,
            headers=headers,
            json={"query": query, "variables": variables},
            timeout=30,
        )
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text}")

        payload = response.json()
        if "errors" in payload:
            log.warning("GraphQL errors: %s", payload["errors"])

        items = j_get(path, payload)
        if not items:
            break

        nodes = items.get("nodes") or []
        all_nodes.extend(nodes)
        log.info(
            "Fetched %d nodes (total %d)",
            len(nodes),
            len(all_nodes),
        )

        page_info = items.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not cursor:
            break

        if delay_sec:
            time.sleep(delay_sec)

    return all_nodes
