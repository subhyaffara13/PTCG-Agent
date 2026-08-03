from typing import Optional

def _next_unquoted_char(text: str, chs: Optional[str], startidx: int = 0) -> int:
    """Return position of next unquoted character in tuple, or -1 if not found.
    
    It is always assumed that the first character being checked is not already
    inside quotes.
    """
    in_quotes = False
    if chs is None:
        chs = string.whitespace

    for i, c in enumerate(text[startidx:]):
        if c == '"' and not _is_character_escaped(text, startidx + i):
            in_quotes = not in_quotes
        if not in_quotes:
            if c in chs:
                return startidx + i
    return -1

