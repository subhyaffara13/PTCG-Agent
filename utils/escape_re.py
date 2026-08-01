
def escapeRE(string: str) -> str:
    string = REGEXP_ESCAPE_RE.sub("\\$&", string)
    return string

