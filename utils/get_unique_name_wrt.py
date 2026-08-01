
def get_unique_name_wrt(
    prefix: str, *containers: Any, requires_suffix: bool = False
) -> str:
    """
    Return a name that starts with `prefix` and is not in any of the
    `containers` (e.g., map, set).
    """
    if not requires_suffix and not is_in(prefix, *containers):
        return prefix

    for i in itertools.count():
        candidate = f"{prefix}_{i}"
        if not is_in(candidate, *containers):
            return candidate

    raise AssertionError("unreachable")

