
def _preceding_ok(state: StateInline, bscan_len: int) -> bool:
    """Check whether the character before the back-scanned portion allows an autolink."""
    abs_pos = state.pos - bscan_len
    if abs_pos <= 0:
        return True
    preceding = state.src[abs_pos - 1]
    return check_prev(preceding)

