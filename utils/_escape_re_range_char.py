
def _escape_re_range_char(c: str) -> str:
    return fr"\{c}" if c in r"\^-][" else c

