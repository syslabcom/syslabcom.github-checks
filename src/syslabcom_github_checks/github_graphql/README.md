# github_graphql

Reusable GitHub GraphQL client. Provides authenticated requests,
pagination, and a JMESPath helper for extracting data from responses.

## Usage

```python
from syslabcom_github_checks.github_graphql import (
    get_headers,
    query_graphql_all,
)

headers = get_headers()
nodes = query_graphql_all(
    query=MY_QUERY,
    variables={"owner": "plone", "projectNumber": 28},
    path="data.organization.projectV2.items",
    headers=headers,
)
```

## API

- `get_headers(token=None)` -- resolves a GitHub token and returns auth
  headers. Accepts an explicit token, or falls back to `GITHUB_TOKEN` /
  `GH_TOKEN` env vars. Raises `ValueError` if no token is found.
- `query_graphql(query, variables, path, *, headers=None)` -- single
  GraphQL request, returns result at `path` (JMESPath). Raises
  `RuntimeError` on non-200 responses.
- `query_graphql_all(query, variables, path, *, headers=None, delay_sec=0.0)`
  -- paginated variant, returns a flat list of all nodes across pages.
- `j_get(path, json_data=None)` -- JMESPath wrapper for extracting
  values from nested dicts.
