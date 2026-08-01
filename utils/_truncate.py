
def _truncate(message: str, length: int) -> str:
    if len(message) > length:
        return message[: length - 3] + "..."
    return message


def _truncate(w, needed):
    """Truncate window by 1 sample if needed for DFT-even symmetry"""
    if needed:
        return w[:-1]
    else:
        return w

