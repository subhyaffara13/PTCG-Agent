
def _numeric_prefix_len(split: list[str]) -> int:
    """Count leading numeric components in a :func:`_version_split` result.

    >>> _numeric_prefix_len(["0", "1", "2", "a1"])
    3
    """
    count = 0
    for segment in split:
        if not segment.isdigit():
            break
        count += 1
    return count


def _numeric_prefix_len(split: list[str]) -> int:
    """Count leading numeric components in a :func:`_version_split` result.

    >>> _numeric_prefix_len(["0", "1", "2", "a1"])
    3
    """
    count = 0
    for segment in split:
        if not segment.isdigit():
            break
        count += 1
    return count

