
def _detect_task_checkbox(src: str, pos: int, maximum: int) -> bool | None:
    """Detect ``[ ]``, ``[x]``, or ``[X]`` at *pos*, followed by whitespace.

    Returns ``True`` (checked), ``False`` (unchecked), or ``None`` (no match).
    """
    # Need at least 4 chars: `[`, char, `]`, whitespace
    if pos + 4 > maximum:
        return None
    if src[pos] != "[":
        return None
    inner = src[pos + 1]
    if src[pos + 2] != "]":
        return None
    if inner == " ":
        checked = False
    elif inner in ("x", "X"):
        checked = True
    else:
        return None
    # After `]`, must have whitespace
    if src[pos + 3] not in (" ", "\t"):
        return None
    return checked

