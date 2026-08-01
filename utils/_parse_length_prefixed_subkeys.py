
def _parse_length_prefixed_subkeys(s: str) -> list[str]:
    """Parse a length-prefixed subkey list.

    The wire format is ``<len>:<subkey>[,<len>:<subkey>...]``.

    Returns:
        A list of subkey strings.
    """
    subkeys: list[str] = []
    pos = 0
    while pos < len(s):
        colon = s.index(":", pos)
        length = int(s[pos:colon])
        start = colon + 1
        subkeys.append(s[start : start + length])
        pos = start + length
        if pos < len(s) and s[pos] == ",":
            pos += 1  # skip comma separator
    return subkeys

