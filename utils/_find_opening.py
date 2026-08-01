
def _find_opening(tokens: Sequence[Token], index: int) -> int | None:
    """Find the opening token index, if the token is closing."""
    if tokens[index].nesting != -1:
        return index
    level = 0
    while index >= 0:
        level += tokens[index].nesting
        if level == 0:
            return index
        index -= 1
    return None

