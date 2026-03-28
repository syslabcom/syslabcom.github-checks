"""GraphQL query strings for the contributors-wanted aggregator."""

# Fetches all cards from a project board. Only requests the fields
# needed by the contributors-wanted tool
ALL_CARDS_QUERY = """
query($owner: String!, $projectNumber: Int!, $itemsCursor: String) {
    organization(login: $owner) {
        projectV2(number: $projectNumber) {
            items(first: 100, after: $itemsCursor) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                nodes {
                    fieldValues(first: 20) {
                        nodes {
                            __typename
                            ... on ProjectV2ItemFieldSingleSelectValue {
                                name
                                field {
                                    ... on ProjectV2SingleSelectField { name }
                                }
                            }
                            ... on ProjectV2ItemFieldDateValue {
                                date
                                field { ... on ProjectV2Field { name } }
                            }
                        }
                    }
                    content {
                        __typename
                        ... on Issue {
                            title
                            number
                            url
                            state
                            createdAt
                            updatedAt
                            author { login }
                            assignees(first: 10) {
                                nodes { login }
                            }
                            labels(first: 20) {
                                nodes { name }
                            }
                            repository {
                                nameWithOwner
                            }
                        }
                    }
                }
            }
        }
    }
}
"""
