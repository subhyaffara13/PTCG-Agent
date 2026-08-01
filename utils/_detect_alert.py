
def _detect_alert(state: StateBlock, startLine: int) -> str | None:
    """Detect ``[!TYPE]`` on *startLine* (after ``>`` prefix has been stripped).

    Returns the alert type string (e.g. ``"NOTE"``) or ``None``.
    """
    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]
    src = state.src

    # Trim trailing whitespace
    while maximum > pos and src[maximum - 1] in (" ", "\t"):
        maximum -= 1

    if maximum - pos < 4:
        return None
    if src[pos] != "[" or src[pos + 1] != "!":
        return None
    if src[maximum - 1] != "]":
        return None
    type_str = src[pos + 2 : maximum - 1].upper()
    if type_str not in _ALERT_TYPES:
        return None
    return type_str

