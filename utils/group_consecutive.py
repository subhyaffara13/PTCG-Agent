
def group_consecutive(items: list[tuple[int, str, str]]) -> list[ImportFromBucket]:
    """Group consecutive items by kind (first element) into ImportFromBuckets.

    Each item is a (kind, name, as_name) tuple.
    """
    result: list[ImportFromBucket] = []
    i = 0
    while i < len(items):
        kind = items[i][0]
        i0 = i
        i += 1
        while i < len(items) and items[i][0] == kind:
            i += 1
        result.append(
            ImportFromBucket(kind, [t[1] for t in items[i0:i]], [t[2] for t in items[i0:i]])
        )
    return result

