"""Data model for contributor cards."""

from dataclasses import dataclass, field


@dataclass
class ContributorCard:
    """A card from a project board for the contributors tool."""

    key: str  # e.g. "plone/volto#1234"
    title: str
    url: str
    repository: str
    number: int
    state: str
    board_status: str | None
    labels: list[str] = field(default_factory=list)
    author: str = ""
    assignees: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    start_date: str | None = None
    fix_date: str | None = None
    project_name: str = ""

    @classmethod
    def from_graphql(cls, node, project_name):
        """Build a ContributorCard from a raw GraphQL node."""
        content = node.get("content") or {}
        repo = (content.get("repository") or {}).get(
            "nameWithOwner", ""
        )
        number = content.get("number", 0)
        field_values = _extract_field_values(node)

        labels_data = (
            (content.get("labels") or {}).get("nodes") or []
        )
        labels = [l["name"] for l in labels_data if "name" in l]

        assignees_data = (
            (content.get("assignees") or {}).get("nodes") or []
        )
        assignees = [
            a["login"] for a in assignees_data if "login" in a
        ]

        return cls(
            key=f"{repo}#{number}",
            title=content.get("title", ""),
            url=content.get("url", ""),
            repository=repo,
            number=number,
            state=content.get("state", ""),
            board_status=field_values.get("Status"),
            labels=labels,
            author=(content.get("author") or {}).get(
                "login", ""
            ),
            assignees=assignees,
            created_at=content.get("createdAt", ""),
            updated_at=content.get("updatedAt", ""),
            start_date=field_values.get("Start Date"),
            fix_date=field_values.get("Fix Date"),
            project_name=project_name,
        )

    def to_dict(self):
        """Convert to a plain dict for JSON serialization."""
        return {
            "key": self.key,
            "title": self.title,
            "url": self.url,
            "repository": self.repository,
            "number": self.number,
            "state": self.state,
            "board_status": self.board_status,
            "labels": self.labels,
            "author": self.author,
            "assignees": self.assignees,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "start_date": self.start_date,
            "fix_date": self.fix_date,
            "project_name": self.project_name,
        }


def _extract_field_values(node):
    """Extract project field values from a raw GraphQL node."""
    result = {}
    field_values = (node.get("fieldValues") or {}).get("nodes") or []

    for fv in field_values:
        typename = fv.get("__typename", "")

        # get field name e.g. "Status", "Start Date"
        field_info = fv.get("field") or {}
        field_name = field_info.get("name")
        if not field_name:
            continue

        # get the actual value based on field type
        if typename == "ProjectV2ItemFieldSingleSelectValue":
            result[field_name] = fv.get("name")
        elif typename == "ProjectV2ItemFieldDateValue":
            result[field_name] = fv.get("date")

    return result
