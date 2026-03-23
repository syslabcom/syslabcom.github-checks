"""Fetch, filter, and normalize contributor cards from project boards."""

import logging

from ..github_graphql.client import query_graphql_all
from .config import BOARDS, CONTRIBUTORS_LABEL, REPOSITORIES
from .models import ContributorCard
from .queries import ALL_CARDS_QUERY

log = logging.getLogger(__name__)

# JMESPath to reach the items connection in the GraphQL response
ITEMS_PATH = "data.organization.projectV2.items"


def collect(*, headers=None, boards=None):
    """Fetch contributor cards from all configured boards."""
    boards = boards or BOARDS
    all_cards = []

    for board in boards:
        org = board["org"]
        project_num = board["project_num"]
        project_name = f"{org}/{project_num}"
        log.info("Fetching board %s", project_name)

        try:
            nodes = query_graphql_all(
                ALL_CARDS_QUERY,
                {"owner": org, "projectNumber": project_num},
                ITEMS_PATH,
                headers=headers,
            )
        except RuntimeError:
            log.warning(
                "Failed to fetch board %s, skipping",
                project_name,
            )
            continue

        for node in nodes:
            content = node.get("content") or {}

            # Skip non-issues (PRs, DraftIssues)
            if content.get("__typename") != "Issue":
                continue

            # Skip repos not in the allow-list
            repo = (content.get("repository") or {}).get(
                "nameWithOwner", ""
            )
            lower_repos = [r.lower() for r in REPOSITORIES]
            if lower_repos and repo.lower() not in lower_repos:
                continue

            # Check for matching label (case-insensitive)
            labels = [
                l["name"]
                for l in (
                    (content.get("labels") or {}).get("nodes")
                    or []
                )
                if "name" in l
            ]
            lower_labels = [l.lower() for l in labels]
            if CONTRIBUTORS_LABEL.lower() not in lower_labels:
                continue

            card = ContributorCard.from_graphql(
                node, project_name
            )
            all_cards.append(card)

    return all_cards
