
def _check_domain(data: str, allow_short: bool) -> int | None:
    """Validate a domain name and return the length consumed, or ``None``."""
    if not data:
        return None

    np = 0
    uscore1 = 0
    uscore2 = 0

    for i, ch in enumerate(data):
        if ch == "_":
            uscore2 += 1
        elif ch == ".":
            uscore1 = uscore2
            uscore2 = 0
            np += 1
        elif not _is_valid_hostchar(ch) and ch != "-":
            if uscore1 == 0 and uscore2 == 0 and (allow_short or np > 0):
                return i
            return None
        # else: valid hostchar or '-'

    if (uscore1 > 0 or uscore2 > 0) and np <= 10:
        return None
    if allow_short or np > 0:
        return len(data)
    return None

