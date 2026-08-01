
def is_escaped(state: StateInline, back_pos: int, mod: int = 0) -> bool:
    """Test if dollar is escaped."""
    # count how many \ are before the current position
    backslashes = 0
    while back_pos >= 0:
        back_pos = back_pos - 1
        if state.src[back_pos] == "\\":
            backslashes += 1
        else:
            break

    if not backslashes:
        return False

    # if an odd number of \ then ignore
    if (backslashes % 2) != mod:  # noqa: SIM103
        return True

    return False

