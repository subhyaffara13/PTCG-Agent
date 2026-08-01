
def split_directive(s: str) -> tuple[list[str], list[str]]:
    """Split s on commas, except during quoted sections.

    Returns the parts and a list of error messages."""
    parts = []
    cur: list[str] = []
    errors = []
    i = 0
    while i < len(s):
        if s[i] == ",":
            parts.append("".join(cur).strip())
            cur = []
        elif s[i] == '"':
            i += 1
            while i < len(s) and s[i] != '"':
                cur.append(s[i])
                i += 1
            if i == len(s):
                errors.append("Unterminated quote in configuration comment")
                cur.clear()
        else:
            cur.append(s[i])
        i += 1
    if cur:
        parts.append("".join(cur).strip())

    return parts, errors

