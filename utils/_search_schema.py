
def _search_schema(schema, matcher):
    """Breadth-first search routine."""
    values = deque([schema])
    while values:
        value = values.pop()
        if not isinstance(value, dict):
            continue
        yield from matcher(value)
        values.extendleft(value.values())

