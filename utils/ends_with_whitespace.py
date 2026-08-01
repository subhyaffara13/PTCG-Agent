
def ends_with_whitespace(it: Any) -> bool:
    """Returns ``True`` if the given item ``it`` is a ``Table`` or ``AoT`` object
    ending with a ``Whitespace``.
    """
    if isinstance(it, Whitespace):
        return True
    if isinstance(it, Table):
        previous = it.value._previous_item()
        return previous is not None and ends_with_whitespace(previous)
    return isinstance(it, AoT) and len(it) > 0 and ends_with_whitespace(it[-1])

