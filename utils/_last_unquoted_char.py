
def _last_unquoted_char(text: str, chs: Optional[str]) -> int:
    """Return position of last unquoted character in list, or -1 if not found."""
    i = len(text) - 1
    in_quotes = False
    if chs is None:
        chs = string.whitespace
    while i > 0:
        if text[i] == '"' and not _is_character_escaped(text, i):
            in_quotes = not in_quotes
            
        if not in_quotes:
            if text[i] in chs:
                return i
        i -= 1
    return -1

