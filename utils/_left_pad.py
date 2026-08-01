
def _left_pad(split: list[str], target_numeric_len: int) -> list[str]:
    """Pad a :func:`_version_split` result with ``"0"`` segments to reach
    ``target_numeric_len`` numeric components.  Suffix segments are preserved.

    >>> _left_pad(["0", "1", "a1"], 4)
    ['0', '1', '0', '0', 'a1']
    """
    numeric_len = _numeric_prefix_len(split)
    pad_needed = target_numeric_len - numeric_len
    if pad_needed <= 0:
        return split
    return [*split[:numeric_len], *(["0"] * pad_needed), *split[numeric_len:]]


def _left_pad(split: list[str], target_numeric_len: int) -> list[str]:
    """Pad a :func:`_version_split` result with ``"0"`` segments to reach
    ``target_numeric_len`` numeric components.  Suffix segments are preserved.

    >>> _left_pad(["0", "1", "a1"], 4)
    ['0', '1', '0', '0', 'a1']
    """
    numeric_len = _numeric_prefix_len(split)
    pad_needed = target_numeric_len - numeric_len
    if pad_needed <= 0:
        return split
    return [*split[:numeric_len], *(["0"] * pad_needed), *split[numeric_len:]]

