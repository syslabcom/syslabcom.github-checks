import jmespath


def j_get(path, json_data=None):
    """Extract data from JSON using a JMESPath expression."""
    expr = jmespath.compile(path)
    return expr.search(json_data)
